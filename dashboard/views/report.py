from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from report.models import Report, GradeCategories, LessionCategories, MajorCategories
from django.db.models.aggregates import Avg
from django.db.models import Q



class SecontReportList(LoginRequiredMixin, ListView):
    """ for list the secund report list  """
    template_name = 'dashboard/report/03-karnameye-sanavilist.html'
    context_object_name = 'items'

    def get_queryset(self):
        self.queryset = Report.objects.filter(user=self.request.user).prefetch_related('user', 'quiz', 'grade',  'major', 'lession').all()
        return self.queryset
    
    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        queryset_list = self.queryset.values_list('percent', flat=True)
 
        context = {
            'count_good_result': self.queryset.filter(Q(status=Report.ReportStatus.good)|Q(status=Report.ReportStatus.excellent)).count(),
            'percent_avg': (sum(queryset_list) // (len(queryset_list) * 100))*100 ,
            'grade':       GradeCategories.objects.filter(is_active=True).all(),
            'lession':   LessionCategories.objects.filter(is_active=True).all(),
            'major':       MajorCategories.objects.filter(is_active=True).all(),
            'status':   Report.ReportStatus,
        }
        data.update(context)

        return data


class FirstReportList(TemplateView):
    template_name = 'dashboard/report/05-karnameye-avalilist.html'

class FirstReportDetail(TemplateView):
    template_name = 'dashboard/report/06-karnameye-avali-detail.html'

class SecondRespotDetail(TemplateView):
    template_name = 'dashboard/report/04-karnameye-sanavi-detail.html'
 
class ThirdReport(TemplateView):
    template_name = 'dashboard/report/02-karnameye-sales.html'