from django import forms
from sitesetting.models import Site, SiteLaw, Team, QuestionAndAnswer
from django.core.validators import FileExtensionValidator
from django_ckeditor_5.widgets import CKEditor5Widget
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import RegionalPhoneNumberWidget, PhoneNumberPrefixWidget

class SiteModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        excluded_widgets = (CKEditor5Widget, forms.CheckboxInput, )
        for field in self.fields.values():

            if  not isinstance(field.widget, excluded_widgets):
                field.widget.attrs.update({'class': 'form-control col-md-4 p-2 m-2'})
            elif  isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'p-2 m-2'})
            

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

class QuestionAndAnswerModelForm(forms.ModelForm):pass
class TeamModelForm(forms.ModelForm):pass
class SiteLawModelForm(forms.ModelForm):pass