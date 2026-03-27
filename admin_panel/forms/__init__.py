from . import users

from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

class BaseForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        excluded_widgets = (CKEditor5Widget, forms.CheckboxInput, )
        for field in self.fields.values():

            if  not isinstance(field.widget, excluded_widgets):
                field.widget.attrs.update({'class': 'form-control col-md-4 p-2 m-2'})
            elif  isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input form-switch p-2 m-2'})