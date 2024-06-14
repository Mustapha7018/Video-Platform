from django.test import TestCase, Client
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser, TemporalUserModel as CodeEmail
from .views import generate_activation_code
from django.utils import timezone
from datetime import timedelta

class AccountViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.verify_url = reverse('verify')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.video_list_url = reverse('video_list')
        self.forgot_password_url = reverse('forgot-password')
        self.reset_password_url = 'reset-password'

        # Create a test user
        self.test_user = CustomUser.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='password123'
        )

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_pages/register.html')

    def test_register_view_post(self):
        response = self.client.post(self.register_url, {
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.verify_url)
        self.assertTrue(CodeEmail.objects.filter(email='newuser@example.com').exists())

    def test_register_view_post_password_mismatch(self):
        data = {
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password124'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.register_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Passwords do not match.")

    def test_register_view_post_invalid_email(self):
        data = {
            'email': 'invalidemail',
            'password1': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.register_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid email address format.")



    def test_code_verification_view_get(self):
        response = self.client.get(self.verify_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_pages/code_verification.html')

    def test_code_verification_view_post(self):
        generated_code = generate_activation_code()
        CodeEmail.objects.create(
            email='newuser@example.com',
            password='password123',
            code=generated_code,
            expiration_date=timezone.now() + timedelta(hours=24)
        )
        session = self.client.session
        session['email'] = 'newuser@example.com'
        session.save()

        response = self.client.post(self.verify_url, {
            'input1': str(generated_code)[0],
            'input2': str(generated_code)[1],
            'input3': str(generated_code)[2],
            'input4': str(generated_code)[3],
            'input5': str(generated_code)[4],
            'input6': str(generated_code)[5],
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(CustomUser.objects.filter(email='newuser@example.com').exists())


    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_pages/login.html')

    def test_login_view_post(self):
        response = self.client.post(self.login_url, {
            'email': 'testuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.video_list_url)

    def test_logout_view_post(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.home_url, response.url)

    def test_forgot_password_view_get(self):
        response = self.client.get(self.forgot_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_pages/email_verification.html')

    def test_forgot_password_view_post(self):
        response = self.client.post(self.forgot_password_url, {
            'email': 'testuser@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(self.reset_password_url, kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(self.test_user.pk)),
            'token': default_token_generator.make_token(self.test_user)
        }))

    def test_password_reset_confirm_view_get(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.test_user.pk))
        token = default_token_generator.make_token(self.test_user)
        response = self.client.get(reverse(self.reset_password_url, kwargs={
            'uidb64': uidb64,
            'token': token
        }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_pages/reset_password.html')

    def test_password_reset_confirm_view_post(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.test_user.pk))
        token = default_token_generator.make_token(self.test_user)
        response = self.client.post(reverse(self.reset_password_url, kwargs={
            'uidb64': uidb64,
            'token': token
        }), {
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(self.client.login(email='testuser@example.com', password='newpassword123'))