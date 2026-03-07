from django.views.generic import TemplateView




class FirstReportList(TemplateView):
    template_name = 'dashboard/report/05-karnameye-avalilist.html'

class FirstReportDetail(TemplateView):
    template_name = 'dashboard/report/06-karnameye-avali-detail.html'

class SecontReportList(TemplateView):
    template_name = 'dashboard/report/03-karnameye-sanavilist.html'

class SecondRespotDetail(TemplateView):
    template_name = 'dashboard/report/04-karnameye-sanavi-detail.html'
 
class ThirdReport(TemplateView):
    template_name = 'dashboard/report/02-karnameye-sales.html'