from django.shortcuts import render
from django.views.generic import TemplateView


class Login(TemplateView):
    template_name =  'main/auth/login.html'

class Register(TemplateView):
    template_name =  'main/auth/register.html'

class OTP(TemplateView):
    template_name =  'main/auth/otp.html'

class ForgotPassword(TemplateView):
    template_name =  'main/auth/forgot-password.html'

class AccountActivation(TemplateView):
    template_name =  'main/auth/account-activation.html'