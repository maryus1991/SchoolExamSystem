from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.LoginWithOTP.as_view() , name='login'),
    path('logout/', views.Logout.as_view() , name='logout'),
    path('login/password', views.LoginWithPassword.as_view() , name='login-password'),
    path('register/', views.Register.as_view() , name='register'),
    path('otp/<str:private_code>', views.OTP.as_view() , name='otp'),
    path('forgot-password/', views.ForgotPassword.as_view() , name='forgot-password'),
    path('account-activation/', views.AccountActivation.as_view() , name='account-activation'),
]
