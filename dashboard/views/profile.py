from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages

# Create your views here.


class Dashboard(TemplateView):
    template_name = 'dashboard/profile/01-profile.html'


class Profile(TemplateView):
    template_name = 'dashboard/profile/11-account.html'