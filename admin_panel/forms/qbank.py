from django import forms
from qbank.models import  QuestionBank, QuestionAnswerKey, QuestionOption, QuestionLessonCategory, QuestionPossible
from django_ckeditor_5.widgets import CKEditor5Widget
from django.core.validators import FileExtensionValidator

class QuestionBankModelForm(forms.ModelForm):
    possible = forms.ModelChoiceField(
        required=True,
        label='سطح',
        empty_label='سطح',
        queryset=QuestionPossible.objects.filter(is_active=True).all(),
        widget=forms.Select(
            attrs={
                'class':'form-control',
                'placeholder':'سطح'
            }
        )
    )
    category = forms.ModelChoiceField(
        required=True,
        label='درس',
        empty_label='درس',
        queryset=QuestionLessonCategory.objects.filter(is_active=True).all(),
        widget=forms.Select(
            attrs={
                'class':'form-control',
                'placeholder':'درس'
            }
        )
    )

    type_of_question = forms.ChoiceField(
        required=True,
        label="نوع سوال",
        
        choices=QuestionBank.TypeOfQuestions,
        widget=forms.Select(
            attrs={
                'class':'form-control',
                'placeholder':'نوع سوال'
            }
        )
    )

    image = forms.ImageField(
        required=False,
        label='عکس',
        widget=forms.FileInput(
            attrs={
                'class':'form-control',
                'placeholder':'عکس'

                
            }
        ),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "webp", "heic"]
            )
        ],
    )

    pdf_file = forms.FileField(
        required=False,
        label='pdf',
        widget=forms.FileInput(
            attrs={
                'class':'form-control',
                'placeholder':'pdf'
                
            }
        ),
        validators=[
            FileExtensionValidator(
                allowed_extensions=[ 'pdf']
            )
        ],
    )
    description = forms.CharField(
        required=False,
        widget=CKEditor5Widget()
    )

    class Meta:
        model = QuestionBank
        fields=[
            'image', 
            'possible', 
            'category', 
            'pdf_file', 
            'type_of_question', 

            'name', 
            'lesson', 
            'description', 
            'is_active', 
            'has_options', 
            'order', 
            'solving_time'
        ]

        widgets={
        
            'name': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'نام'
                }
            ),
            'lesson': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'مبحث'

                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'has_options': forms.CheckboxInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'order': forms.NumberInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'solving_time': forms.NumberInput(
                attrs={
                    'class':'form-control'
                }
            ),
        }

class QuestionAnwerKeyModelForm(forms.ModelForm):

    type_of_answer = forms.ChoiceField(
        required=True,
        label="نوع پاسخ",
        
        choices=QuestionAnswerKey.TypeOfAnswer,
        widget=forms.Select(
            attrs={
                'class':'form-control',
                'placeholder':'نوع پاسخ'
            }
        )
    )

    image = forms.ImageField(
        required=False,
        label='عکس',
        widget=forms.FileInput(
            attrs={
                'class':'form-control',
                'placeholder':'عکس'

                
            }
        ),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "webp", "heic"]
            )
        ],
    )

    pdf_file = forms.FileField(
        required=False,
        label='pdf',
        widget=forms.FileInput(
            attrs={
                'class':'form-control',
                'placeholder':'pdf'
                
            }
        ),
        validators=[
            FileExtensionValidator(
                allowed_extensions=[ 'pdf']
            )
        ],
    )

    description = forms.CharField(
        required=False,
        widget=CKEditor5Widget()
    )

    class Meta:
        model = QuestionAnswerKey
        fields=['type_of_answer', 'description', 'image', 'pdf_file']
 
class QuestionOptionsModelForm(forms.ModelForm):
    class Meta:
        model= QuestionOption
        fields = ['text' ,'is_correct' ,'order']
        widgets = {
            'text':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'نام'
                }
            ) ,
            'is_correct':forms.CheckboxInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'order':forms.NumberInput(
                attrs={
                    'class':'form-control'
                }
            ),
        }