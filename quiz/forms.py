from django import forms

from quiz.models import GradeCategories, MajorCategories, LessionCategories, Quiz


class QuizSearchForm(forms.Form):
    
    status = forms.ChoiceField(
        required=False,
        label="وضعیت",
        
        choices=Quiz.QuizStatus,
        widget=forms.Select(
            attrs={
                'class':'form-control-custom',
                'placeholder':'وضعیت'
            }
        )
    )

    lession = forms.ModelChoiceField(
        required=False,
        label='درس',
        empty_label='درس',
        queryset=LessionCategories.objects.filter(is_active=True).all(),
        widget=forms.Select(
            attrs={
                'class':'form-control-custom',
                'placeholder':'درس'
            }
        )
    )
    grade = forms.ModelChoiceField(
        required=False,
        label='پایه',
        empty_label='پایه',
        queryset=GradeCategories.objects.filter(is_active=True).all(),
        widget=forms.Select(
            attrs={
                'class':'form-control-custom',
                'placeholder':'پایه'
            }
        )
    )
    major = forms.ModelChoiceField(
        required=False,
        label='رشته',
        empty_label='رشته',
        queryset=MajorCategories.objects.filter(is_active=True).all(),
        widget=forms.Select(
            attrs={
                'class':'form-control-custom',
                'placeholder':''
            }
        )
    )

    name = forms.CharField(
        required=False,
        label="جستجو",
        widget=forms.TextInput(
            attrs={
                'class':'form-control-custom',
                'placeholder':'نام ازمون ...',
            }
        )
    )
 