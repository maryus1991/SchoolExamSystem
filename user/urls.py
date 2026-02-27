from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.Login.as_view() , name='login'),
    path('register/', views.Register.as_view() , name='register'),
    path('otp/', views.OTP.as_view() , name='otp'),
    path('forgot-password/', views.ForgotPassword.as_view() , name='forgot-password'),
    path('account-activation/', views.AccountActivation.as_view() , name='account-activation'),
]
