from . import BaseForm, forms
from report.models import Report

class ReportModelForm(BaseForm, forms.ModelForm):
    
    class Meta:
        model = Report
        exclude = ("id", 'created_at')
