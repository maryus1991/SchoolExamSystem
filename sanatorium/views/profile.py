from django.views.generic import TemplateView
from django.contrib import messages
from dashboard.views.profile import Profile


class SanatoriumPanel(TemplateView):
    template_name =  'sanatorium/profile/01-dashboard.html'

 

class SanatoriumEditProfileInfos(Profile):
    template_name =  'sanatorium/profile/02-account.html'

    
 
