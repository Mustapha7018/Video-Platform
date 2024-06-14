import re
import logging
from django.views import View
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from .models import CustomUser, TemporalUserModel as CodeEmail
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.tokens import default_token_generator
from utils.functions import (
    generate_activation_code,
    is_expired,
    combine_code,
)
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode
)
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView
)

logger = logging.getLogger(__name__)



''' HOMEPAGE VIEW '''
class HomeView(TemplateView):
    template_name = 'video_pages/home.html'



''' REGISTER USER '''
class RegisterView(View):
    template_name = "account_pages/register.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        email_address = request.POST.get("email")
        password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")

        if not email_address:
            messages.error(request, "Email address is required.")
            return redirect(reverse('register'))

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(reverse('register'))

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect(reverse('register'))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
            messages.error(request, "Invalid email address format.")
            return redirect(reverse('register'))

        if CustomUser.objects.filter(email=email_address).exists():
            messages.error(request, "Email already exists.")
            return redirect(reverse('register'))

        generated_code = generate_activation_code()
        expiration_date = timezone.now() + timedelta(hours=24)
        
        context = {
            "generated_code": generated_code,
        }
        html_message = render_to_string("account_pages/code.html", context)
        plain_message = strip_tags(html_message)

        try:
            if CodeEmail.objects.filter(email=email_address).exists():
                code_user = CodeEmail.objects.get(email=email_address)
                code_user.code = generated_code
                code_user.expiration_date = expiration_date
                code_user.save()
            else:
                code_user = CodeEmail.objects.create(
                    email=email_address, 
                    password=password, 
                    code=generated_code,
                    expiration_date=expiration_date
                )
                code_user.save()

            message = EmailMultiAlternatives(
                subject="Email Verification Code",
                body=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[email_address],
            )
            message.attach_alternative(html_message, 'text/html')
            message.send()

            request.session['email'] = email_address  # Store email in session
            messages.success(request, "Email verification code sent to email.")
            return redirect("verify")
        except Exception as e:
            logger.error(f"Error creating CodeEmail or sending email: {e}")
            messages.error(request, f"Error creating CodeEmail or sending email: {e}, please try again.")
            return render(request, self.template_name)

        return render(request, self.template_name)




''' VIEW FOR CODE VERIFICATION '''
class CodeVerificationView(View):
    template_name = "account_pages/code_verification.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        code = combine_code(request)
        email = request.session.get('email')  # Store email in session on registration

        if not email:
            messages.error(request, "Email is required.")
            return redirect('register')

        try:
            code_email = CodeEmail.objects.get(email=email, code=code)
            if is_expired(code_email.expiration_date):
                code_email.delete()
                messages.error(request, "The verification code has expired. Please register again.")
                return redirect('register')

            user = CustomUser.objects.create_user(
                email=code_email.email,
                username=code_email.email,
                password=code_email.password,
            )
            user.save()
            code_email.delete()
            del request.session['email']
            messages.success(request, "Email verified and account created. Please log in.")
            return redirect('login')
        except CodeEmail.DoesNotExist:
            messages.error(request, "Invalid code. Please try again.")
            return redirect('verify')

        return render(request, self.template_name)



''' VIEW TO LOG IN USERS '''
class CustomLoginView(View):
    template_name = 'account_pages/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back " + user.email + "!")
            return redirect('video_list')  
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect(reverse('login'))



''' VIEW TO LOG OUT USERS '''
class LogoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')



''' VIEW TO RESET PASSWORD '''
class ForgotPasswordView(View):
    template_name = "account_pages/email_verification.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = reverse_lazy('reset-password', kwargs={'uidb64': uid, 'token': token})
            messages.success(request, "Go ahead and set reset your password.")
            return redirect(reset_url)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Email address not found.')
            return redirect('forgot-password')



''' VIEW TO CONFIRM PASSWORD RESET '''
class PasswordResetConfirmView(View):
    template_name = "account_pages/reset_password.html"

    def get(self, request, uidb64, token, *args, **kwargs):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        return render(request, self.template_name, context)

    def post(self, request, uidb64, token, *args, **kwargs):
        new_password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if new_password is None or confirm_password is None:
            messages.error(request, "Please fill in both password fields.")
            return redirect('reset-password', uidb64=uidb64, token=token)

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset-password', uidb64=uidb64, token=token)

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect('reset-password', uidb64=uidb64, token=token)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Your password has been reset. Please log in.")
                return redirect('login')
            else:
                messages.error(request, "The reset link is invalid or has expired.")
                return redirect('forgot-password')
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            messages.error(request, "The reset link is invalid or has expired.")
            return redirect('forgot-password')


