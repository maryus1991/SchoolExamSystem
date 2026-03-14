from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, RedirectView
from django.contrib import messages
from dashboard.forms import UpdateUserForm, ChangePassword
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.forms import ChangePhoneNumberNaitnalID 
from user.models import User
from django.contrib.auth import logout
from django.db.models.aggregates import Avg

# Create your views here.


class Dashboard(TemplateView):
    template_name = 'dashboard/profile/01-profile.html'

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)

        quiz = self.request.user.quiz_student.filter(is_active=True)

        data['quiz_count'] = quiz.count()
        data['exams'] = quiz.all()[:6]

        questions_count = 0
        for item in quiz.all():
            questions_count += int(item.questions.count())

        data['questions_count'] = questions_count

        user_report = self.request.user.reports
        data['best_order'] = user_report.order_by('order').first().order
        data['reports'] = user_report.order_by('percent').all()[:6]
        data['avg_exams_percents'] = sum(user_report.values_list('percent', flat=True)) / (100 * len(user_report.values_list('percent', flat=True)))  


        return data


class Profile(LoginRequiredMixin, View):
    template_name = 'dashboard/profile/11-account.html'

    def get(self, request, *args, **kwargs):
        
        context = {

            'update_form': UpdateUserForm( initial={
                'first_name': request.user.first_name,
                'gender': request.user.gender,
                'last_name': request.user.last_name,
                'province': request.user.province,
                'city': request.user.city,
                'school': request.user.school,
                'grade': request.user.grade,
                'major': request.user.major,
                'father_name': request.user.father_name,
                'birth': request.user.birth,
            }),

            'password_form': ChangePassword(),
            'phoneNumber_form': ChangePhoneNumberNaitnalID(
                initial={
                    'PhoneNumber': request.user.PhoneNumber,
                    'national_id': request.user.national_id,
                }
            ),

        }

        return render(request, self.template_name, context)
        
    def post(self, request, *args, **kwargs):
        form = UpdateUserForm(request.POST )
        if form.is_valid():
            request.user.first_name = form.cleaned_data.get( 'first_name')
            request.user.gender = form.cleaned_data.get( 'gender')
            request.user.last_name = form.cleaned_data.get( 'last_name')
            request.user.province = form.cleaned_data.get( 'province')
            request.user.city = form.cleaned_data.get( 'city')
            request.user.school = form.cleaned_data.get( 'school')
            request.user.grade = form.cleaned_data.get( 'grade')
            request.user.major = form.cleaned_data.get( 'major')
            request.user.father_name = form.cleaned_data.get( 'father_name')
            request.user.birth = form.cleaned_data.get( 'birth')
            request.user.save()

            
            messages.success(
                request, 'تغییرات ثبت شد'
            )

        else:
            messages.error(
                request, form.errors
            )

        return self.get(request, *args, **kwargs)

class ChangePasswordView(LoginRequiredMixin, View):
    """for change the password"""
    
    def post(self, request , *args, **kwargs):

        form = ChangePassword(request.POST)

        if form.is_valid():
            
 
            if request.user.check_password(form.cleaned_data.get('current_password')):
                request.user.set_password(form.cleaned_data.get('password'))
                request.user.save()

                messages.success(request, 'رمز عبور شما با موفقیت بروز رسانی شد')
                
            else:
                messages.error(
                    request, 'رمزعبور فعلی را اشتباه وارد کردید'
                )

        else:
            messages.error(
                request, form.errors
            )

        return redirect('dashboard:profile')

class ChangePhoneNumberNaitnalIDView(LoginRequiredMixin, View):
    """for change the password"""
    
    def post(self, request , *args, **kwargs):

        form = ChangePhoneNumberNaitnalID(request.POST)

        if form.is_valid():
            
            user = User.objects.filter(
                PhoneNumber=form.cleaned_data.get('PhoneNumber')
            )

            if not user.exists():
                user = request.user
                user.PhoneNumber = form.cleaned_data.get('PhoneNumber')
                # user.is_verified = False
                user.save()

                messages.success(
                    request, '  شماره با موفقیت تغییر یافت لطفا   از راه ورود با رمز یک بار مصرف وارد شوید تا حساب شما فعال شود'
                )
                logout(request)
                return redirect('dashboard:profile')



            elif user.exists() and user.first().PhoneNumber != request.user.PhoneNumber:
                messages.error(
                    request, 'این شماره قبلا ثبت نام شده است'
                )
            
            
            user = User.objects.filter(
                national_id=form.cleaned_data.get('national_id')
            )

            if not user.exists()  :
                user = request.user
                user.national_id = form.cleaned_data.get('national_id')
                # user.is_verified = False
                user.save()

                messages.success(
                    request, 'کد ملی با موفقیت تغییر یافت لطفا   از راه ورود با رمز یک بار مصرف وارد شوید تا حساب شما فعال شود'
                )
                logout(request)
                return redirect('dashboard:profile')



            elif user.exists() and user.first().national_id != request.user.national_id:
                messages.error(
                    request, 'این کدملی قبلا ثبت نام شده است'
                )
            

            
        else:
            messages.error(
                request, form.errors
            )

        return redirect('dashboard:profile')