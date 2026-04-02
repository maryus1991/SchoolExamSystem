from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from .models import Team, ContactUs, Site
from quiz.models import Quiz
from .forms import ContactModelForm
from django.urls import reverse_lazy
from django.contrib import messages


class MainPage(TemplateView):
    """
     main page
    """

    template_name = 'main/site/main.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['quiz'] = Quiz.objects.filter(is_active=True).prefetch_related('lession', 'questions').all()[0:3]
        data['site'] = Site.objects.first()

        return data


class Contact(CreateView):
    """
     contact page
    """
    model=ContactUs
    form_class = ContactModelForm
    template_name = 'main/site/contact.html'
    success_url = reverse_lazy('site:contact')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['site'] = Site.objects.first()
        return data

    def form_valid(self, form):
        messages.success(
            self.request,'پیام شما ارسال شد'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
   
 
        messages.error(
            self.request, form.errors.as_text
        )
        return super().form_invalid(form)


class About(TemplateView):
    """
     about page
    """

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['site'] = Site.objects.first()
        data['team'] = Team.objects.filter(is_active=True).all()

        return data

    template_name = 'main/site/about.html'