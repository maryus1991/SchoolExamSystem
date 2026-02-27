from django.shortcuts import render
from django.views.generic import TemplateView


class MainPage(TemplateView):
    """
     main page
    """

    template_name = 'main/site/main.html'

class Contact(TemplateView):
    """
     main page
    """

    template_name = 'main/site/contact.html'

class About(TemplateView):
    """
     main page
    """

    template_name = 'main/site/about.html'