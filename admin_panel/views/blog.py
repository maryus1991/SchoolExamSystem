from django.views.generic import CreateView, ListView, RedirectView, UpdateView, FormView
from django.contrib import messages
from admin_panel.mixins import AdminPermissionRequire
from admin_panel.forms.blog import BlogModelForm
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from blog.models import Blog
from django.utils.timezone import now
from django.db.models.aggregates import Count


class BlogList(AdminPermissionRequire, ListView):
    """blog list view"""

    context_object_name = 'items'
    template_name = 'admin-panel/blog/list.html'
    queryset = Blog.objects.prefetch_related('user').annotate(views_count=Count('views')).all()
    paginate_by = 50

class BlogCreate(AdminPermissionRequire, CreateView):
    """for create blog"""

    template_name = 'admin-panel/blog/create.html'
    model = Blog
    form_class = BlogModelForm
    success_url = reverse_lazy('admin-panel:blog-list')

    def form_valid(self, form):
        messages.success(
            self.request, 'ایتم با موفقیت اضافه شد'
        )
        form.instance.user = self.request.user
        
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, form.errors
        )
        return super().form_invalid(form)

class BlogUpdate(AdminPermissionRequire, UpdateView):
    '''for update blog'''

    template_name = 'admin-panel/blog/create.html'
    model = Blog
    form_class = BlogModelForm
    success_url = reverse_lazy('admin-panel:blog-list')
    context_object_name = 'item'

    def form_valid(self, form):
        messages.success(
            self.request, 'ایتم با موفقیت بروز رسانی شد'
        )
        form.instance.user = self.request.user

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, form.errors
        )
        return super().form_invalid(form)

class BlogDelete(AdminPermissionRequire, RedirectView):
    """for deactivate or activate the blog """

    model = Blog
    success_url = reverse_lazy('admin-panel:blog-list')

    def get_redirect_url(self, *args, **kwargs):

        pk = kwargs.get('pk')

        item = get_object_or_404(self.model, pk=pk)
        item.delete()

        messages.warning(self.request, 'پست مورد نظر حذف شد')

        return self.success_url

class BlogActiveDeactivate(AdminPermissionRequire, RedirectView):
    """for deactivate or activate the blog """

    model = Blog
    success_url = reverse_lazy('admin-panel:blog-list')

    def get_redirect_url(self, *args, **kwargs):

        pk = kwargs.get('pk')

        item = get_object_or_404(self.model, pk=pk)


        if item.is_active:
            item.is_active = False
            messages.success(self.request, 'پست غیر فعال شد')
            item.updated_at = None


        else: 
            item.is_active = True
            messages.success(self.request, '  پست فعال شد و انتشار یافت')
            item.updated_at = now()

        item.save()


        return self.success_url
