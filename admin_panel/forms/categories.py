from django import forms
from quiz.models import GradeCategories, LessionCategories, MajorCategories
from qbank.models import QuestionPossible

class MajorModelForm(forms.ModelForm):
    
    class Meta:
        model = MajorCategories
        fields='__all__'
        widgets = {
            'name':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'نام'
                }
            ),
            
            'order':forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'عدد ترتیبی'
                }
            ),
        }

class GradeModelForm(forms.ModelForm):
    
    class Meta:
        model = GradeCategories
        fields='__all__'
        widgets = {
            'name':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'نام'
                }
            ),
            
            'order':forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'عدد ترتیبی'
                }
            ),
        }

class PossibleModelForm(forms.ModelForm):
    
    class Meta:
        model = QuestionPossible
        fields='__all__'
        widgets = {
            'name':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'نام'
                }
            ),
            
            'order':forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'عدد ترتیبی'
                }
            ),
        }

class LessionModelForm(forms.ModelForm):
    
    class Meta:
        model = LessionCategories
        fields='__all__'
        widgets = {
            'name':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'نام'
                }
            ),
            
            'order':forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'عدد ترتیبی'
                }
            ),
        }
