from django.views.generic import TemplateView
from django.contrib import messages
from dashboard.views.profile import Profile
from sanatorium.mixins import SanatorPermissionRequire



class SanatoriumPanel(SanatorPermissionRequire, TemplateView):
    template_name =  'sanatorium/profile/01-dashboard.html'

class SanatoriumEditProfileInfos(SanatorPermissionRequire, Profile):
    template_name =  'sanatorium/profile/02-account.html'

    
 
