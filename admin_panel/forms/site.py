from django import forms
from sitesetting.models import Site, SiteLaw, Team, QuestionAndAnswer
from django.core.validators import FileExtensionValidator
from django_ckeditor_5.widgets import CKEditor5Widget
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import RegionalPhoneNumberWidget, PhoneNumberPrefixWidget
from . import BaseForm


class SiteModelForm(BaseForm, forms.ModelForm):
    description = forms.CharField(
        required=True,
        label='توضیحات',
        widget=CKEditor5Widget()
    )

    logo = forms.ImageField(
        required=True,
        label='عکس',
        widget=forms.FileInput(
            attrs={
                'class':'form-control',
                'placeholder':'عکس'

                
            }
        ),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["webp" ]
            )
        ],
    )

    phone_number = PhoneNumberField(
        required=True,
        label="شماره ",
        widget=RegionalPhoneNumberWidget(
            attrs={
                'class':'form-control',
                'placeholder':' ... شماره',
                'dir':'rtl'
            }
        )
    )


    class Meta:
        model = Site
        exclude = ['id']
        field_classes = {'form-control'}

class QuestionAndAnswerModelForm(BaseForm, forms.ModelForm):
    
    class Meta:
        model = QuestionAndAnswer
        exclude = ['id']

class TeamModelForm(BaseForm, forms.ModelForm):

    avatar = forms.ImageField(
        required=True,
        label='عکس',
        widget=forms.FileInput(
            attrs={
                'class':'form-control',
                'placeholder':'عکس'
            }
        ),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["webp", 'jpeg', 'png', 'jpg', 'heic' ]
            )
        ],
    )

    phone_number = PhoneNumberField(
        required=True,
        label="شماره ",
        widget=RegionalPhoneNumberWidget(
            attrs={
                'class':'form-control',
                'placeholder':' ... شماره',
                'dir':'rtl'
            }
        )
    )

    class Meta:
        model = Team
        exclude = ['id']
        
class SiteLawModelForm(BaseForm, forms.ModelForm):

    description = forms.CharField(
        required=True,
        label='توضیحات',
        widget=CKEditor5Widget()
    )

    class Meta:
        model = SiteLaw
        exclude = ['id']