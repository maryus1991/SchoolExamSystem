from django.views.generic import TemplateView, UpdateView, CreateView, ListView
from admin_panel.forms.site import SiteModelForm, SiteLawModelForm, TeamModelForm, QuestionAndAnswerModelForm
from django.contrib import messages
from admin_panel.mixins import AdminPermissionRequire
from sitesetting.models import Site, Team, QuestionAndAnswer, SiteLaw
from django.urls import reverse_lazy

class Main(TemplateView):
    template_name = 'admin-panel/main.html'

class SiteUpdateView(AdminPermissionRequire, UpdateView):
    """for update the site settings """

    context_object_name = 'item'
    template_name = 'admin-panel/settings/index.html'
    form_class = SiteModelForm
    success_url = reverse_lazy('admin-panel:site')

    def get_object(self):
        return Site.objects.first()

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'تغییرات اعمال شد')
        return super().form_valid(form)
    
# team 
class TeamListView(AdminPermissionRequire, ListView):
    """list view for team"""

    queryset = Team.objects.all()
    context_object_name = 'items'
    template_name = 'admin-panel/settings/team/list.html'
    paginate_by = 100
class TeamCreateView(AdminPermissionRequire, CreateView):
 
    queryset = Team.objects.all()
    context_object_name = 'items'
    template_name = 'admin-panel/settings/team/create.html'
    form_class = TeamModelForm
    success_url = reverse_lazy('admin-panel:site-team-list')

    def form_valid(self, form):
        messages.success(self.request, 'ایتم اضافه شد')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
class TeamUpdateView(AdminPermissionRequire, UpdateView):
 
    queryset = Team.objects.all()
    context_object_name = 'items'
    template_name = 'admin-panel/settings/team/create.html'
    form_class = TeamModelForm
    success_url = reverse_lazy('admin-panel:site-team-list')


    def form_valid(self, form):
        messages.success(self.request, 'ایتم اضافه شد')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

# Q&A    
class QuestionAndAnswerListView(AdminPermissionRequire, ListView):
    """list view for QuestionAndAnswer"""

    queryset = QuestionAndAnswer.objects.all()
    context_object_name = 'items'
    template_name = 'admin-panel/settings/Q&A/list.html'
    paginate_by = 100
    
class QuestionAndAnswerCreateView(TeamCreateView):
  
    context_object_name = 'items'
    template_name = 'admin-panel/settings/Q&A/create.html'
    form_class = QuestionAndAnswerModelForm
    success_url = reverse_lazy('admin-panel:site-qa-list')

class QuestionAndAnswerUpdateView(TeamUpdateView):
 

    queryset = QuestionAndAnswer.objects.all()
    context_object_name = 'items'
    template_name = 'admin-panel/settings/Q&A/create.html'
    form_class = QuestionAndAnswerModelForm
    success_url = reverse_lazy('admin-panel:site-qa-list')


# site law
class SiteLawListView(AdminPermissionRequire, ListView):
    """list view for SiteLaw"""

    queryset = SiteLaw.objects.all()
    context_object_name = 'items'
    template_name = 'admin-panel/settings/law/list.html'
    paginate_by = 100
class SiteLawCreateView(TeamCreateView):
  
    context_object_name = 'items'
    template_name = 'admin-panel/settings/law/create.html'
    form_class = SiteLawModelForm
    success_url = reverse_lazy('admin-panel:site-law-list')

class SiteLawUpdateView(TeamUpdateView):
 

    queryset = SiteLaw.objects.all()
    context_object_name = 'items'
    template_name = 'admin-panel/settings/law/create.html'
    form_class = SiteLawModelForm
    success_url = reverse_lazy('admin-panel:site-law-list')



    