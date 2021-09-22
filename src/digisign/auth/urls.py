from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from digisign.auth.views import StaffTokenObtainPairView, RegularTokenObtainPairView

app_name = 'auth'

urlpatterns = [
    path('token/staff/', StaffTokenObtainPairView.as_view(), name='login_staff'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('token/regular/', RegularTokenObtainPairView.as_view(), name='login_customer'),
    # path('register/', CustomerRegisterView.as_view(), name='register_customer'),
    # path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    # path('forgot-password/<employee>/', ForgotPasswordView.as_view(), name='forgot_password'),
    # path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    # path('reset-password/<token>/<uuid>/', ResetPasswordView.as_view(), name='password_reset'),
    # path('verify/email/<token>/<uuid>/', VerifyEmailView.as_view(), name='verify_email'),
    # path('otp-verification/', OTPVerifyView.as_view(), name='otp_verification'),
    # path('set-password/', SetPasswordView.as_view(), name='set_password')
]
