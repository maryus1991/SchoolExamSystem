from  admin_panel.forms.report import ReportModelForm
from report.models import Report
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib import messages
from django.urls import reverse
from admin_panel.mixins import AdminPermissionRequire

class ReportListView(AdminPermissionRequire, ListView):
    """list view for reports"""

    context_object_name = 'items'
    template_name = 'admin-panel/reports/list.html'
    paginate_by = 100

    def get_queryset(self):
        query = Report.objects
        if quiz_id:= self.kwargs.get('quiz_id'):
            query = query.filter(quiz__id=quiz_id)

        return query.prefetch_related('user', 'quiz', 'grade', 'major', 'lession').all()


class ReportCreateView(AdminPermissionRequire, CreateView):
    """for create report by admin"""

    form_class = ReportModelForm
    template_name = 'admin-panel/reports/create.html'
    model = Report


    def form_valid(self, form):
        messages.success(self.request, 'کارنامه ایجاد شد')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse('admin-panel:report-list')
        
    

class ReportUpdateView(AdminPermissionRequire, UpdateView):
    """for update report by admin"""

    form_class = ReportModelForm
    template_name = 'admin-panel/reports/create.html'
    model = Report


    def form_valid(self, form):
        messages.success(self.request, 'کارنامه بروز رسانی شد')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('admin-panel:report-list')
        