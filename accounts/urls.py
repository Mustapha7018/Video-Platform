from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', CodeVerificationView.as_view(), name='verify'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('resend-verification/', ResendVerificationView.as_view(),
            name='resend-verification'),
    path('forgot-password/', ForgotPasswordView.as_view(),
            name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
            name='reset-password'),
]
