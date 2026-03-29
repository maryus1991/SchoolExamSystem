from . import users
from jalali_date.fields import JalaliDateField, JalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime, AdminSplitDateTime
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

class BaseForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        excluded_widgets = (CKEditor5Widget, forms.CheckboxInput, )
        
        for field_name, field in self.fields.items():
            
            if  not isinstance(field.widget, excluded_widgets):
                field.widget.attrs.update({'class': 'form-control col-md-4 p-2 m-2'})
            elif  isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input form-switch p-2 m-2'})

            if isinstance(field, (forms.DateField)):
                self.fields[field_name] = JalaliDateField(
                    widget=AdminJalaliDateWidget(
                        attrs=field.widget.attrs
                    ),
                    initial=field.initial,
                    required=field.required,
                    label=field.label,
                    help_text=field.help_text,
                )
            if isinstance(field, (forms.DateTimeField)):
                self.fields[field_name] = JalaliDateTimeField(
                    widget=AdminJalaliDateWidget(
                        attrs=field.widget.attrs
                    ),
                    initial=field.initial,
                    required=field.required,
                    label=field.label,
                    help_text=field.help_text,
                )
 