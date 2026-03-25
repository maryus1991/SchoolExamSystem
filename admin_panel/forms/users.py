from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.validators import validate_phonenumber
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from user.models import User, GradeCategories, MajorCategories


class CreateUserForm(forms.Form):

    PhoneNumber = PhoneNumberField(
        required=True,
        label="شماره ... ",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':' ... شماره',
                'dir':'rtl'
            }
        )
    )
    gender = forms.ChoiceField(
        required=True,
        label="جنسیت",
        choices=User.GenderOfUser,
        widget=forms.Select(
            attrs={
                'class':'form-control',
                'placeholder':'جنسیت'
            }
        )
    )
    type_of_user = forms.ChoiceField(
        required=True,
        label="نوع حساب",
        choices=User.TypeOfUser,
        widget=forms.Select(
            attrs={
                'class':'form-control',
                'placeholder':'نوع حساب'
            }
        )
    )
    password = forms.CharField(
        required=True,
        label="رمز عبور",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'رمز عبور'
            }
        )
    )
    province = forms.CharField(
        required=True,
        label="استان",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'استان'
            }
        )
    )
    national_id = forms.CharField(
        required=True,
        label="کدملی",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'کدملی'
            }
        )
    )
    city = forms.CharField(
        required=True,
        label="شهر",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'شهر'
            }
        )
    )
    first_name = forms.CharField(
        required=True,
        label="نام ",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'نام'
            }
        )
    )
    last_name = forms.CharField(
        required=True,
        label="نام خانوادگی",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'نام خانوادگی'
            }
        )
    )
    school = forms.CharField(
        required=True,
        label="مدرسه",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'مدرسه'
            }
        )
    )
    father_name = forms.CharField(
                required=True,
        label="نام پدر",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
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
                'class':'form-control',
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
                'class':'form-control',
                'placeholder':'رشته'
            }
        )
    )
    birth = JalaliDateField(
        required=True,
        label="تاریخ تولد",
        widget=AdminJalaliDateWidget(
            attrs={
                "class": "form-control",
                "dir": "rtl",
                'placeholder':'تاریخ تولد'

            }
        ),
    )   
   
    def clean_phone_number(self):
        phone_number = self.cleaned_data["PhoneNumber"]
        validate_phonenumber(phone_number)

        return phone_number

class UpdateUserForm(forms.Form):

    PhoneNumber = PhoneNumberField(
        required=True,
        label="شماره ... ",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':' ... شماره',
                'dir':'rtl'
            }
        )
    )
    gender = forms.ChoiceField(
        required=True,
        label="جنسیت",
        choices=User.GenderOfUser,
        widget=forms.Select(
            attrs={
                'class':'form-control',
                'placeholder':'جنسیت'
            }
        )
    )
    type_of_user = forms.ChoiceField(
        required=True,
        label="نوع حساب",
        choices=User.TypeOfUser,
        widget=forms.Select(
            attrs={
                'class':'form-control',
                'placeholder':'نوع حساب'
            }
        )
    )
    password = forms.CharField(
        required=False,
        label="رمز عبور",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'رمز عبور'
            }
        )
    )
    province = forms.CharField(
        required=True,
        label="استان",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'استان'
            }
        )
    )
    national_id = forms.CharField(
        required=True,
        label="کدملی",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'کدملی'
            }
        )
    )
    city = forms.CharField(
        required=True,
        label="شهر",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'شهر'
            }
        )
    )
    first_name = forms.CharField(
        required=True,
        label="نام ",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'نام'
            }
        )
    )
    last_name = forms.CharField(
        required=True,
        label="نام خانوادگی",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'نام خانوادگی'
            }
        )
    )
    school = forms.CharField(
        required=True,
        label="مدرسه",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'مدرسه'
            }
        )
    )
    father_name = forms.CharField(
                required=True,
        label="نام پدر",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
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
                'class':'form-control',
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
                'class':'form-control',
                'placeholder':'رشته'
            }
        )
    )
    birth = JalaliDateField(
        required=True,
        label="تاریخ تولد",
        widget=AdminJalaliDateWidget(
            attrs={
                "class": "form-control",
                "dir": "rtl",
                'placeholder':'تاریخ تولد'

            }
        ),
    )   
   
    def clean_phone_number(self):
        phone_number = self.cleaned_data["PhoneNumber"]
        validate_phonenumber(phone_number)

        return phone_number
    


