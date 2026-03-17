from django.views.generic import TemplateView
from django.contrib import messages
from dashboard.views.profile import Profile
from sanatorium.mixins import SanatorPermissionRequire
from quiz.models import Quiz
from report.models import Report
from sanatorium.models import SanatoriumWallet
from sitesetting.models import Ticket



class SanatoriumPanel(SanatorPermissionRequire, TemplateView):
    template_name =  'sanatorium/profile/01-dashboard.html'

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)

        return data

class SanatoriumEditProfileInfos(SanatorPermissionRequire, Profile):
    template_name =  'sanatorium/profile/02-account.html'

    
 
