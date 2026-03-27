from django.views.generic import  RedirectView, ListView, View
from admin_panel.mixins import AdminPermissionRequire
from user.models import User, GradeCategories, MajorCategories
from django.shortcuts import render, get_object_or_404
from admin_panel.forms.users import CreateUserForm, UpdateUserForm
from django.contrib import messages
from django.urls import reverse

class UserListView(AdminPermissionRequire, ListView):
    """for list the users"""

    context_object_name = 'items'
    template_name = 'admin-panel/users/list.html'
    queryset = User.objects.prefetch_related('major', 'grade').all()
    paginate_by = 200

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['type'] = User.TypeOfUser
        data['gender'] = User.GenderOfUser

        return data
    
class UserCreate(AdminPermissionRequire, View):
    """for create user"""

    template_name = 'admin-panel/users/create.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form' : CreateUserForm(request.POST or None)
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):

        form = CreateUserForm(request.POST or None)
        
        if form.is_valid():

            PhoneNumber = form.cleaned_data.pop('PhoneNumber')
            national_id = form.cleaned_data.get('national_id')
            password = form.cleaned_data.pop('password')

            if User.objects.filter(PhoneNumber=PhoneNumber).exists():
                messages.error(request, 'این شماره قبلا در سایت موجود می باشد')
                return self.get(request, *args, **kwargs)
            
            if User.objects.filter(national_id=national_id).exists():
                messages.error(request, 'این کد ملی قبلا در سایت موجود می باشد')
                return self.get(request, *args, **kwargs)

            user = User(PhoneNumber=PhoneNumber, **form.cleaned_data)
            user.set_password(password)
            user.save() 
            messages.success(request, 'کاربر ثبت شد')

        else:
            messages.error(request, form.errors)
        
        return self.get(request, *args, **kwargs)

class UserUpdate(AdminPermissionRequire, View):
    """for update user"""

    template_name = 'admin-panel/users/create.html'
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = get_object_or_404(User, pk=pk)

        initial = {
                'PhoneNumber':user.PhoneNumber, 
                'gender':user.gender, 
                'type_of_user':user.type_of_user, 
                'province':user.province, 
                'national_id':user.national_id,  
                'city':user.city, 
                'first_name':user.first_name, 
                'last_name':user.last_name,  
                'school':user.school,  
                'father_name':user.father_name, 
                'grade':user.grade,  
                'major':user.major,  
                'birth':user.birth,  
        }
        context = {
            'form' : UpdateUserForm(request.POST or initial)
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        form = UpdateUserForm(request.POST or None)
        
        if form.is_valid():

            PhoneNumber = form.cleaned_data.get('PhoneNumber')
            national_id = form.cleaned_data.get('national_id')
            password = form.cleaned_data.pop('password')
            user = User.objects.get(pk=pk)

            if user.PhoneNumber != PhoneNumber and User.objects.filter(PhoneNumber=PhoneNumber).exists():
                messages.error(request, 'این شماره قبلا در سایت موجود می باشد')
                return self.get(request, *args, **kwargs)
            
            if user.national_id != national_id and  User.objects.filter(national_id=national_id).exists():
                messages.error(request, 'این کد ملی قبلا در سایت موجود می باشد')
                return self.get(request, *args, **kwargs)

            if password and not user.check_password(password):
                user.set_password(password)
                
            for field in form.cleaned_data:
                if hasattr(user, field) and getattr(user, field) != form.cleaned_data[field]   :
                    setattr(user, field, form.cleaned_data[field])

            
            user.save() 
            messages.success(request, 'کاربر بروز رسانی شد')

        else:
            messages.error(request, form.errors)
        
        return self.get(request, *args, **kwargs)

class UserActiveDeactivate(AdminPermissionRequire, RedirectView):
    """for deactivate or activate the user"""

    def get_redirect_url(self, *args, **kwargs):

        pk = kwargs.get('pk')

        user = get_object_or_404(User, pk=pk)

        if user == self.request.user:
            messages.info(self.request, 'شما نمی توانید این تغییرات را روی کاربر خود اعمال کنید')

            return reverse('admin-panel:user-list')


        if user.is_active:
            user.is_active = False
            messages.info(self.request, 'کاربر غیر فعال شد')
        else: 
            user.is_active = True
            messages.info(self.request, 'کاربر فعال شد')
            
        user.save()


        return reverse('admin-panel:user-list')

class UserVerifyUnverify(AdminPermissionRequire, RedirectView):

    """for deactivate or activate the user"""

    def get_redirect_url(self, *args, **kwargs):

        pk = kwargs.get('pk')

        user = get_object_or_404(User, pk=pk)
        
        if user == self.request.user:
            messages.info(self.request, 'شما نمی توانید این تغییرات را روی کاربر خود اعمال کنید')

            return reverse('admin-panel:user-list')


        if user.is_verified:
            user.is_verified = False
            messages.info(self.request, 'شماره حساب غیر فعال شد')
        else: 
            user.is_verified = True
            messages.info(self.request, 'شماره حساب فعال شد')

        user.save()


        return reverse('admin-panel:user-list')
    


    """for list the users"""

    context_object_name = 'items'
    template_name = 'admin-panel/users/list.html'
    queryset = User.objects.prefetch_related('major', 'grade').all()
    paginate_by = 200

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['type'] = User.TypeOfUser
        data['gender'] = User.GenderOfUser

        return data