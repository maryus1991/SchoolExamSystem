from django.views.generic import DeleteView, RedirectView, ListView, DetailView, View
from admin_panel.mixins import AdminPermissionRequire
from user.models import User
from django.shortcuts import render
from admin_panel.forms import users


class UserListView(AdminPermissionRequire, ListView):
    """for list the users"""

    context_object_name = 'items'
    template_name = 'admin-panel/users/list.html'
    queryset = User.objects.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['type'] = User.TypeOfUser

        return data
    

class UserCreate(AdminPermissionRequire, View):
    """for create user"""

    template_name = 'admin-panel/users/create.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class UserUpdate(AdminPermissionRequire, View):
    """for create user"""

    template_name = 'admin-panel/users/create.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)