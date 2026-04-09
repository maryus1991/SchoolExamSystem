from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from report.models import Report, GradeCategories, LessionCategories, MajorCategories
from django.db.models.aggregates import Avg
from django.db.models import Q
import math


class SecontReportList(LoginRequiredMixin, ListView):
    """ for list the secund report list  """
    template_name = 'dashboard/report/03-karnameye-sanavilist.html'
    context_object_name = 'items'
    paginate_by = 50


    def get_queryset(self):
        self.queryset = Report.objects.filter(user=self.request.user).prefetch_related('user', 'quiz', 'grade',  'major', 'lession').all()
        return self.queryset
    
    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        queryset_list = self.queryset.values_list('percent', flat=True)
 
        context = {
            'count_good_result': self.queryset.filter(Q(status=Report.ReportStatus.good)|Q(status=Report.ReportStatus.excellent)).count(),
            'percent_avg': (sum(list(queryset_list)) // ((len(list(queryset_list)) if len(list(queryset_list))>0 else 0.01  ) * 100))*100 ,
            'grade':       GradeCategories.objects.filter(is_active=True).all(),
            'lession':   LessionCategories.objects.filter(is_active=True).all(),
            'major':       MajorCategories.objects.filter(is_active=True).all(),
            'status':   Report.ReportStatus,
        }
        data.update(context)

        return data

class ThirdReport(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/report/02-karnameye-sales.html'

    def get_context_data(self, **kwargs) -> dict[str, ...]:
        context = super().get_context_data(**kwargs)
        user_reports = Report.objects.filter(user=self.request.user).prefetch_related('quiz')  
        percents_list = list(user_reports.values_list('percent', flat=True))
        score_list = list(user_reports.values_list('score', flat=True))


        context["avg_percent"] = sum(percents_list) / len(percents_list) if len(percents_list) > 0 else 1
        context["avg_score"] = sum(score_list) / len(score_list) if len(score_list) > 0 else 1
        
        context["best_order"] = user_reports.order_by('-order').first().order if user_reports else 0  
        context["best_teraze"] = user_reports.order_by('-teraze').first().teraze if user_reports else 0
        context["best_percent"] = max(percents_list) if len(percents_list) > 0 else 0 
        context["best_score"] = max(score_list) if len(score_list) > 0 else 0

        context["report_list"] = user_reports.order_by('-pk').annotate(teraze_avg=Avg('teraze')).all()[:25] 
  
        return context
    



#####
# class FirstReportList(TemplateView):
#     template_name = 'dashboard/report/05-karnameye-avalilist.html'

# class FirstReportDetail(TemplateView):
#     template_name = 'dashboard/report/06-karnameye-avali-detail.html'

# class SecondRespotDetail(TemplateView):
#     template_name = 'dashboard/report/04-karnameye-sanavi-detail.html'
#####