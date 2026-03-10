from django import forms
from .models import QuestionLessonCategory, QuestionPossible, QuestionBank


class QBankSearchForm(forms.Form):
    
    type_ = forms.ChoiceField(
        required=False,
        label="نوع سوال",
        
        choices=QuestionBank.TypeOfQuestions,
        widget=forms.Select(
            attrs={
                'class':'form-control-custom',
                'placeholder':'نوع سوال'
            }
        )
    )

    possible = forms.ModelChoiceField(
        required=False,
        label='سطح دشواری',
        empty_label='همه سطوح',
        queryset=QuestionPossible.objects.filter(is_active=True).all(),
        widget=forms.Select(
            attrs={
                'class':'form-control-custom',
                'placeholder':'سطح دشواری'
            }
        )
    )
    grade = forms.ModelChoiceField(
        required=False,
        label='درس',
        empty_label='همه دروس',
        queryset=QuestionLessonCategory.objects.filter(is_active=True).all(),
        widget=forms.Select(
            attrs={
                'class':'form-control-custom',
                'placeholder':'درس'
            }
        )
    )
 
    name = forms.CharField(
        required=False,
        label="جستجو",
        widget=forms.TextInput(
            attrs={
                'class':'form-control-custom',
                'placeholder':'سوال ...',
            }
        )
    )
 