from django.views.generic import TemplateView
from django.contrib import messages
from dashboard.views.profile import Profile
from sanatorium.mixins import SanatorPermissionRequire
from quiz.models import Quiz, StudentAnswer
 
from sanatorium.models import SanatoriumWallet
from sitesetting.models import Ticket
from django.db.models import Q


class SanatoriumPanel(SanatorPermissionRequire, TemplateView):
    template_name =  'sanatorium/profile/01-dashboard.html'

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)

        quiz_list = Quiz.objects.filter(
            Q(sanatorium=self.request.user) 

        )
        
        data["need_correcting"] = quiz_list.filter(
            Q(status=Quiz.QuizStatus.FINISHED) | Q(status=Quiz.QuizStatus.WAITING_CORRECTION)
        )

        data['corrected_quiz'] = quiz_list.filter(
            Q(status=Quiz.QuizStatus.CORRECTED) | Q(status=Quiz.QuizStatus.RESULTS_PUBLISHED)
        ).count()
        
        data['report_count'] = StudentAnswer.objects.filter(corrected_by=self.request.user).all().count()

        walltes = SanatoriumWallet.objects.filter(user=self.request.user)
        for item in walltes.filter(status=SanatoriumWallet.OrderStatus.active).all() : item.get_payment_price()
        data['unpaid_wallets'] = sum(walltes.filter(status=SanatoriumWallet.OrderStatus.active).values_list('final_price', flat=True))
        

        data["quiz_list"] = quiz_list.order_by('-pk').all()[:3]
        data['wallets'] = walltes.order_by('-pk').all()[:6]
        data['tickets'] = Ticket.objects.filter(user=self.request.user).order_by('-pk').all()[:6]
        

        return data

class SanatoriumEditProfileInfos(SanatorPermissionRequire, Profile):
    template_name =  'sanatorium/profile/02-account.html'

    
 
