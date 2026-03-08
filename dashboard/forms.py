
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.validators import validate_phonenumber
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from user.models import User, GradeCategories, MajorCategories
from sitesetting.models import Ticket, TicketChat, TicketProblemCategory, TicketProblemPlacement
from django.core.validators import FileExtensionValidator

class TicketForm(forms.Form):


    priority = forms.ChoiceField(
        required=True,
        label="اهمیت",
        choices=Ticket.TicketPriority,
        widget=forms.Select(
            attrs={
                'class':'form-control-custom',
                'placeholder':'اهمیت'
            }
        )
    )

    problem = forms.ModelChoiceField(
        required=True,
        label='دسته‌بندی',
        empty_label='دسته‌بندی',
        queryset=TicketProblemCategory.objects.filter(is_active=True).all(),
        widget=forms.Select(
            attrs={
                'class':'form-control-custom',
                'placeholder':'دسته‌بندی'
            }
        )
    )

    placement = forms.ModelChoiceField(
        required=True,
        label=' بخش مرتبط ',
        empty_label=' بخش مرتبط ',
        queryset=TicketProblemPlacement.objects.filter(is_active=True).all(),
        widget=forms.Select(
            attrs={
                'class':'form-control-custom',
                'placeholder':' بخش مرتبط '
            }
        )
    )

    file = forms.FileField(
        required=False,
        label='پیوست',
        widget=forms.FileInput(
            attrs={
                'class':'hidden',
                'id':'attachInput'
                
            }
        ),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "webp", "heic", 'pdf']
            )
        ],
    )

    description = forms.CharField(
        required=True,
        label="پیام ... ",
        widget=forms.Textarea(
            attrs={
                'class':'form-control-custom',
                'placeholder':'مشکل خود را با جزئیات بیشتر شرح دهید. هر چه اطلاعات دقیق‌تری ارائه دهید، تیم پشتیبانی سریع‌تر می‌تواند کمک کند',
                'id':"msgBody",
                'rows':"6"
            }
        )
    )

    name = forms.CharField(
        required=True,
        label="موضوع تیکت",
        widget=forms.TextInput(
            attrs={
                'class':'form-control-custom',
                'placeholder':'موضوع را به‌طور کوتاه بیان کنید',
            }
        )
    )
 

class TicketChatForm(forms.Form):
    message = forms.CharField(
        required=True,
        label="پیام ... ",
        widget=forms.Textarea(
            attrs={
                'class':'form-control-custom',
                'placeholder':'پیام خود را بنویسید...',
                'id':"msgInput",
                'rows':"1"
            }
        )
    )


class ChangePhoneNumberNaitnalID(forms.Form):
    PhoneNumber = PhoneNumberField(
        required=True,
        label="شماره ... ",
        widget=forms.TextInput(
            attrs={
                'class':'form-control-custom',
                'placeholder':' ... شماره',
                'dir':'rtl'
            }
        )
    )

    national_id = forms.CharField(
        required=True,
        label="کدملی",
        widget=forms.TextInput(
            attrs={
                'class':'form-control-custom',
                'placeholder':'کدملی'
            }
        )
    )
 

    
    def clean_phone_number(self):
        phone_number = self.cleaned_data["PhoneNumber"]
        validate_phonenumber(phone_number)

        return phone_number


class UpdateUserForm(forms.Form):


    gender = forms.ChoiceField(
        required=True,
        label="جنسیت",
        choices=User.GenderOfUser,
        widget=forms.Select(
            attrs={
                'class':'form-control-custom',
                'placeholder':'جنسیت'
            }
        )
    )

    province = forms.CharField(
        required=True,
        label="استان",
        widget=forms.TextInput(
            attrs={
                'class':'form-control-custom',
                'placeholder':'استان'
            }
        )
    )



    city = forms.CharField(
        required=True,
        label="شهر",
        widget=forms.TextInput(
            attrs={
                'class':'form-control-custom',
                'placeholder':'شهر'
            }
        )
    )
    first_name = forms.CharField(
        required=True,
        label="نام ",
        widget=forms.TextInput(
            attrs={
                'class':'form-control-custom',
                'placeholder':'نام'
            }
        )
    )
    last_name = forms.CharField(
        required=True,
        label="نام خانوادگی",
        widget=forms.TextInput(
            attrs={
                'class':'form-control-custom',
                'placeholder':'نام خانوادگی'
            }
        )
    )

    school = forms.CharField(
        required=True,
        label="مدرسه",
        widget=forms.TextInput(
            attrs={
                'class':'form-control-custom',
                'placeholder':'مدرسه'
            }
        )
    )

    father_name = forms.CharField(
                required=True,
        label="نام پدر",
        widget=forms.TextInput(
            attrs={
                'class':'form-control-custom',
                'placeholder':'نام پدر'
            }
        )
    )


    grade = forms.ModelChoiceField(
        required=True,
        label='پایه',
        queryset=GradeCategories.objects.filter(is_active=True).all(),
        empty_label='انتخاب پایه',
        widget=forms.Select(
            attrs={
                'class':'form-control-custom',
                'placeholder':'پایه'
            }
        )
    )

    major = forms.ModelChoiceField(
        required=True,
        label='رشته',
        empty_label='انتخاب رشته',
        queryset=MajorCategories.objects.filter(is_active=True).all(),
        widget=forms.Select(
            attrs={
                'class':'form-control-custom',
                'placeholder':'رشته'
            }
        )
    )

    birth = JalaliDateField(
        required=True,
        label="تاریخ تولد",
        widget=AdminJalaliDateWidget(
            attrs={
                "class": "form-control-custom",
                "dir": "rtl",
                'placeholder':'تاریخ تولد'

            }
        ),
    )


class ChangePassword(forms.Form):

    current_password = forms.CharField(
        required=True,
        label="رمز عبور فعلی",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control-custom',
                'placeholder':'رمز عبور فعلی'
            }
        )
    )

    password = forms.CharField(
        required=True,
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control-custom',
                'placeholder':'رمز عبور'
            }
        )
    )

 

    def clean_password(self):
        password = self.cleaned_data["password"]

 
        if len(password) < 8:
            raise forms.ValidationError("رمز شما باید حداقل 8 کاراکتر باشد")

        if password.isdigit():
            raise forms.ValidationError(
                "رمز شما باید شامل حروف بزرگ و کوچک و اعداد انگلیسی باشد"
            )

        if password.isupper():
            raise forms.ValidationError(
                "رمز شما باید شامل حروف بزرگ و کوچک و اعداد انگلیسی باشد"
            )

        if password.islower():
            raise forms.ValidationError(
                "رمز شما باید شامل حروف بزرگ و کوچک و اعداد انگلیسی باشد"
            )

        return password