from django import forms
from quiz.models import StudentAnswer

class SanatoriumCorecctingPanelForm(forms.Form):

    satantorium_message = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'feedback-area mt-3',
                'row': 3,
                'id': 'feedbackText',
                'placeholder': "بازخورد خود را برای این دانش‌آموز بنویسید...",

            }
        )
    )

    score = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': "score-display",
                'id': "scoreDisplay" ,        
            }
        )
    )

    corrected = forms.ChoiceField(
        required=True,
        label=StudentAnswer.TypeOfCorrect.not_corrected,
        choices= StudentAnswer.TypeOfCorrect,
        widget=forms.Select(
            attrs={
                'class':'form-control-custom mt-3',
                'placeholder':'وضعیت'
            }
        )
    )