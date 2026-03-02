from django import forms
from .models import ContactUs



class ContactModelForm(forms.ModelForm):
    class Meta:
        model=ContactUs
        exclude = ['admin_read']
        widgets = {
            'subject':forms.TextInput(
                attrs={
                    'placeholder':'موضوع پیام',
                    'class':'form-control-custom'
                }
            ),
            'name':forms.TextInput(
                attrs={
                    'placeholder':'نام و نام خانوادگی',
                    'class':'form-control-custom col-span-6'
                }
            ),
            'phone':forms.TextInput(
                attrs={
                    'placeholder':'شماره',
                    'class':'form-control-custom col-span-6',
                    # 'dir':'ltr'
                }
            ),
            'message':forms.Textarea(
                attrs={
                    'placeholder':'پیام خود را بنویسید...',
                    'class':'form-control-custom',
                    'rows':"5"
                }
            )
        }