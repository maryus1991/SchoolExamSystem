from django.views.generic import TemplateView, UpdateView
from admin_panel.forms.site import SiteModelForm
from django.contrib import messages
from admin_panel.mixins import AdminPermissionRequire
from sitesetting.models import Site

class Main(TemplateView):
    template_name = 'admin-panel/main.html'

class SiteUpdateView(AdminPermissionRequire, UpdateView):
    """for update the site settings """

    context_object_name = 'item'
    template_name = 'admin-panel/settings/index.html'
    form_class = SiteModelForm

    def get_object(self):
        return Site.objects.first()

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'تغییرات اعمال شد')
        return super().form_valid(form)
    
        
    