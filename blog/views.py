from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Blog, BlogView
from ipware import get_client_ip

class BlogListView(ListView):
    """
    blog list view
    """

    paginate_by = 25
    queryset = Blog.objects.filter(is_active=True).all()
    template_name = 'main/blog/list.html'
    context_object_name = 'items'


class BlogDetail(DetailView):
    """
    blog detail
    """

    def dispatch(self, request, *args, **kwargs):
    
        try:
            ip, is_rout = get_client_ip(self.request)
            view = BlogView.objects.get_or_create(ip=ip, blog_id=self.kwargs["pk"])

            if not view[1]:
                view[0].count += 1
                view[0].save()

            if view[0].count == 0:
                view[0].count = 1
                view[0].save()

        except Exception as e:
            pass    
    
        return super().dispatch(request, *args, **kwargs)
    

    queryset = Blog.objects.filter(is_active=True).all()
    template_name = 'main/blog/detail.html'
    context_object_name = 'item'
    