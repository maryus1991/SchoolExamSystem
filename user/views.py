from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView, RedirectView
from django.urls import reverse
from .models import User
from django.contrib import messages
from sitesetting.models import Site
from .forms import CreateUserForm, OTPForm, LoginOTP, LoginPassword
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.transaction import atomic
from django.utils.crypto import get_random_string
from config.settings import OTP_EXPIRATIONS_SECONDS, LOGIN_TEMP
from django.utils.timezone import now
from django.contrib.auth import login, logout

class Logout(LoginRequiredMixin, RedirectView):
    """for log out the user"""

    def get_redirect_url(self, *args, **kwargs):
        
        next_url = self.request.GET.get('next')

        logout(self.request)

        messages.info(
            self.request, 'با موفقیت از حساب خود خارج شدید'
        )
        
        if next_url:
            return next_url

        return reverse('site:main')


class LoginWithOTP(View):
    template_name =  'main/auth/login-otp.html'

    def get(self, request, *args, **kwargs):
        context = {
            'site':Site.objects.first(),
            'form':LoginOTP(request.POST or None),
            'next_url' : request.GET.get('next')
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        
        next_url = request.GET.get('next')

        if request.user.is_authenticated:
            messages.info(request, 'شما وارد سایت هستید')
            if next_url:
                return redirect(next_url)

            return self.get(request, *args, **kwargs)
        
        form = LoginOTP(request.POST or None)
        if form.is_valid():
            PhoneNumber = form.cleaned_data.get('PhoneNumber')
            user = User.objects.filter(PhoneNumber=PhoneNumber)

            if not user.exists() or user.count() != 1:
                messages.error(
                    request, 'کاربر پیدا نشد'
                )
                return self.get(request, *args, **kwargs)

            user = user.first()

            if not user.is_active:
                messages.error(request, 'حساب شما غیر فعال شده است با ادمین در اتباط باشید')
                return self.get(request, *args, **kwargs)
        
            if user.login_temp > LOGIN_TEMP:
                messages.error(request, 'به دلیل تعداد ورود های ناموفق که داشتید حساب شما غیر فعال شده است لطفا با ادمین در ارتباط باشید')
                return self.get(request, *args, **kwargs)

            
            user.private_code = get_random_string(1000)
            user.save()

            if next_url:
                return redirect(reverse('user:otp', kwargs={'private_code':user.private_code}) + '?next=' + next_url   )

            else:
                return redirect(reverse('user:otp', kwargs={'private_code':user.private_code}))



        else:
            messages.error(
                request, form.errors
            )
            return self.get(request, *args, **kwargs)        


class LoginWithPassword(View):
    template_name =  'main/auth/login-password.html'

    def get(self, request, *args, **kwargs):
        context = {
            'site': Site.objects.first(),
            'form': LoginPassword(request.POST or None),
            'next_url' : request.GET.get('next')
        }

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        
        next_url = request.GET.get('next')
 

        if request.user.is_authenticated:
            messages.info(request, 'شما وارد سایت هستید')
            if next_url:
                return redirect(next_url)

            return self.get(request, *args, **kwargs)

 
        
        form = LoginPassword(request.POST or None)
        if form.is_valid():
            PhoneNumber = form.cleaned_data.get('PhoneNumber')
            user = User.objects.filter(PhoneNumber=PhoneNumber)

            if not user.exists() or user.count() != 1:
                messages.error(
                    request, 'کاربر پیدا نشد'
                )
                return self.get(request, *args, **kwargs)

            user = user.first()

            if not user.is_active:
                messages.error(request, 'حساب شما غیر فعال شده است با ادمین در اتباط باشید')
                return self.get(request, *args, **kwargs)
            
            if user.login_temp > LOGIN_TEMP:
                messages.error(request, 'به دلیل تعداد ورود های ناموفق که داشتید حساب شما غیر فعال شده است لطفا با ادمین در ارتباط باشید')
                return self.get(request, *args, **kwargs)

        
            if not user.is_verified:
                messages.error(request, 'حساب شما تایید نشده است لطفا ورود خود را با رمز یک بار مصرف انجام دهید')
                return self.get(request, *args, **kwargs)

            password = form.cleaned_data.get('password')

            if not user.check_password(password):

                if user.login_temp > LOGIN_TEMP:
                    user.is_verified=False
                    user.is_active=False
                else:
                    user.login_temp+=1

                user.save()
                messages.error(request, 'رمز عبور خود را اشتباه وارد کردید ')
                messages.info(request, f'شما {int(LOGIN_TEMP) - int(user.login_temp) } فرصت دیگر برای ورود به سایت دارید که بعد از ان حساب شما غیر فعال می شود')
                return self.get(request, *args, **kwargs)
            
            messages.success(request, 'خوش امدید')
            login(request, user)
            user.login_temp = 0
            user.save()

            if next_url:
                return redirect(next_url)
            
            return redirect('dashboard:main')

        
        else:
            messages.error(
                request, form.errors
            )
            return self.get(request, *args, **kwargs)        


class Register(View):
    template_name =  'main/auth/register.html'

    def get(self, request, *args, **kwargs):
        
   
        context = {
            'form': CreateUserForm(request.POST or None),
            'site':Site.objects.first(),
            'next_url' : request.GET.get('next')

        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
    
        form = CreateUserForm(request.POST or None)
        
        next_url = request.GET.get('next')

        if request.user.is_authenticated:
            messages.info(request, 'شما وارد سایت هستید')
            if next_url:
                return redirect(next_url)

            return self.get(request, *args, **kwargs)

        if form.is_valid():
            form_data = form.cleaned_data

            try:
                
                national_id = form_data.get('national_id')
                PhoneNumber = form_data.get('PhoneNumber')

                if User.objects.filter(national_id=national_id).exists():
                    messages.error(request, 'این کدملی قبلا در سایت ثبت نام کرده است')

                    return self.get(request, *args, **kwargs)

                
                if User.objects.filter(PhoneNumber=PhoneNumber).exists():
                    messages.error(request, 'این شماره قبلا در سایت ثبت نام کرده است')
                
                    return self.get(request, *args, **kwargs)



                with atomic():
                    password = form_data.pop('password')
                   
                    user = User.objects.get_or_create(
                        **form_data
                    ) 

       

                    if not user[1]:
                        messages.error(request, 'کاریری با این اطلاعات قبلا در سایت ثبت نام کرده است')
                        return self.get(request, *args, **kwargs)

                    
                    user[0].set_password(password)
                    user[0].private_code = get_random_string(1000)
                    user[0].save()

                    messages.success(request, 'حساب با موفقیت ساخته شد')

                    if next_url:
                        return redirect(reverse('user:otp', kwargs={'private_code':user[0].private_code}) + '?next=' + next_url )
                    
                    else:
                        return redirect(reverse('user:otp', kwargs={'private_code':user[0].private_code}))

                   

            except Exception as E:
                messages.error(request, 'مشکلی پیش اومد لطفا در اطلاعات ورودی دقت فرمایید و دوباره امتحان نمایید')
                print(self.__class__.__name__, E)
                return self.get(request, *args, **kwargs)

                    
        else:

            messages.error(request, form.errors)
            return self.get(request, *args, **kwargs)


class OTP(View):
    template_name =  'main/auth/otp.html'


    def dispatch(self, request, *args, **kwargs):
        private_code = kwargs.get('private_code')
        self.user = get_object_or_404(
            User, private_code=private_code
        )        
        
        if self.user.login_temp > LOGIN_TEMP:
            messages.error(request, 'به دلیل تعداد ورود های ناموفق که داشتید حساب شما غیر فعال شده است لطفا با ادمین در ارتباط باشید')
            return redirect('site:main')
        
        if not self.user.is_active:
            messages.error(request, 'حساب شما غیر فعال شده است با ادمین در اتباط باشید')
            return redirect('site:main')
        
        next_url = request.GET.get('next')
        
        if request.user.is_authenticated:
            messages.info(request, 'شما وارد سایت هستید')
            if next_url:
                return redirect(next_url)

            return self.get(request, *args, **kwargs)
        
        if self.user.otp_expiry_date is None or self.user.otp_expiry_date < now():
 
            self.otp_result = self.user.set_otp()



        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        timer = self.user.otp_expiry_date - now()

        messages.info(
            request, 'برای شما کد ارسال شده است با وارد کردن ان حساب شما فعال خواهد شد '
        )
        context = {
            'timer': timer.seconds ,
            'PhoneNumber': self.user.PhoneNumber,
            'form': OTPForm(request.POST or None),
            'private_code':self.user.private_code
        }

        return render(request, self.template_name, context)        

    def post(self, request, *args, **kwargs):
        next_url = request.GET.get('next')

        form = OTPForm(request.POST or None) 
        if form.is_valid():
          
            result = self.user.verify_otp(form.cleaned_data.get('otp'))

            if result[0] == 200:
                login(request, self.user)

                if next_url:
                    messages.success(
                        request, 'خوش امدید'
                    )
                    return redirect(next_url)

                return redirect('user:account-activation')
            else:
                messages.error(request, result[1])
                return self.get(request, *args, **kwargs)
        else:
            messages.error(request, form.errors)
            return self.get(request, *args, **kwargs)


class ForgotPassword(View):
    template_name =  'main/auth/forgot-password.html'
    form = LoginPassword
    otp_form = OTPForm



    def get(self, request, *args, **kwargs):
        next_param = request.GET.get('next') 

        if not next_param:
            next_param = request.POST.get('next') 




        method = 'get'
        form = self.form(request.GET or request.POST or None )
        

        if form.is_valid():

            if request.user.is_authenticated:
                messages.info(request, 'شما وارد سایت هستید')
                if next_param:
                    return redirect(next_param)
            
                return redirect('dashboard:main')

            try:
                error = ' مشکلی پیش اومده لطفا دوباره امتحان کنید'
                user = User.objects.filter(
                    PhoneNumber = form.cleaned_data.get('PhoneNumber')
                ) 
                
                if not user.exists() or user.count() != 1:
                    error = 'کاربر پیدا نشد'
                    raise AttributeError

                user = user.first()

                if not user.is_active :
                    error = 'این حساب غیر فعال است لطفا با ادمین در ارتباط باشید'
                    raise AttributeError
                
                if user.login_temp >= LOGIN_TEMP:
                    error = 'شما پیش از حد مجاز تلاش برای ورود به سایت کردید لطفا با ادمین در ارتباط باشید'
                    raise AttributeError
                
                if user.otp_expiry_date and user.otp_expiry_date <= now():
                    user.set_otp()
                    messages.success(
                        request, 'برای شما کد اعتبار سنجی ارسال شد' 
                    )
                elif user.otp_expiry_date is None:
                    user.set_otp()
                    messages.success(
                        request, 'برای شما کد اعتبار سنجی ارسال شد' 
                    )
 

                method = 'post' 


                    
            except Exception as E:
                print(E)
                messages.error(
                    request, error 
                )


        if  request.GET.get('PhoneNumber') or request.GET.get('password')  :
 
            messages.error(
                request, form.errors
            )

        context = {
            'next_url' : next_param, 
            'form': form , 
            'otp_form': self.otp_form(request.POST or None) , 
            'method': method
        }

        if method == 'post':
            context.update({
                'PhoneNumber': str(form.cleaned_data.get('PhoneNumber')).replace(' ', ''),
                'password': form.cleaned_data.get('password')
            })
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        
        form = self.form(request.POST or None)
        form_otp = self.otp_form(request.POST or None)
        

        next_param = request.POST.get('next') 
        
        if request.user.is_authenticated:
            messages.info(request, 'شما وارد سایت هستید')
            if next_param:
                return redirect(next_param)

            return self.get(request, *args, **kwargs)
 
        if form.is_valid(): 

            if form_otp.is_valid():

                try:
                    error = ' مشکلی پیش اومده لطفا دوباره امتحان کنید'
                    user = User.objects.filter(
                        PhoneNumber = form.cleaned_data.get('PhoneNumber')
                    ) 
                    
                    if not user.exists() or user.count() != 1:
                        error = 'کاربر پیدا نشد'
                        raise AttributeError

                    user = user.first()

                    if not user.is_active :
                        error = 'این حساب غیر فعال است لطفا با ادمین در ارتباط باشید'
                        raise AttributeError
                    
                    if user.login_temp >= LOGIN_TEMP:
                        error = 'شما پیش از حد مجاز تلاش برای ورود به سایت کردید لطفا با ادمین در ارتباط باشید'
                        raise AttributeError
                    
                    
                    otp = form_otp.cleaned_data.get('otp')
                    result = user.verify_otp(otp)

                    if result[0] == 200:
                        
                        user.set_password(form.cleaned_data.get('password'))
                        user.save()

                        messages.success(
                            request, 'رمز عبور شما با موفقیت تغییر یافت'
                        )
                        login(request, user)

                        if next_param:
                            return redirect(next_param)
                        return redirect('dashboard:main')
                        

                    else:
                        error = result[1]
                        raise ArithmeticError
        
                        
                except Exception as E:
                
                    messages.error(
                        request, error 
                    )

            else:
                          
                messages.error(
                    request, form_otp.errors
                )

        else:
                
            messages.error(
                request, form.errors
            )



        return self.get(request, *args, **kwargs)


class AccountActivation(TemplateView):
    template_name =  'main/auth/account-activation.html'