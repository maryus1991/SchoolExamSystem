from django.views.generic import TemplateView, CreateView, View
from .models import Team, ContactUs, Site
from quiz.models import Quiz
from .forms import ContactModelForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.http.response import HttpResponsePermanentRedirect
from django.http import HttpResponse
from config.settings import BASE_DIR

class FavIcon(View):
    """for return the favicon.ico"""

    def get(self, *args, **kwargs):
        try:
            logo = Site.objects.first().logo
            return HttpResponsePermanentRedirect(logo.url)
        except:
            with open(BASE_DIR / 'sorna.jpg', 'rb') as f :
                return HttpResponse(f.read(), content_type="image/png")

class MainPage(TemplateView):
    """
     main page
    """

    def dispatch(self, request, *args, **kwargs):
        try:
            site = Site.objects.first()
            if site.message_info :
                messages.info(request, site.message_info)
            if site.message_warning :
                messages.warning(request, site.message_warning)
            if site.message_success :
                messages.success(request, site.message_success)
            if site.message_danger :
                messages.error(request, site.message_danger)
        except: pass
        return super().dispatch(request, *args, **kwargs)
    

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