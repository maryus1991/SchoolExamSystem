from django import forms
from qbank.models import  QuestionBank, QuestionAnswerKey, QuestionOption, QuestionPossible
from django_ckeditor_5.widgets import CKEditor5Widget
from django.core.validators import FileExtensionValidator
from quiz.models import LessionCategories


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
        queryset=LessionCategories.objects.filter(is_active=True).all(),
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
        label='توضیحات',
        widget=CKEditor5Widget()
    )

    class Meta:
        model = QuestionBank
        fields=[
            'name', 
            'lesson', 
            'order', 
            'solving_time',
            
            'has_options', 
            'is_active', 
            
            'type_of_question', 
            'category', 
            'possible',

            'image', 
            'pdf_file', 
            'description', 

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
            'is_active': forms.CheckboxInput(),
            'has_options': forms.CheckboxInput(),
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
        fields=[
            'type_of_answer', 
            'description', 
            'image', 
            'pdf_file']
 
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
            'is_correct':forms.CheckboxInput(),
            'order':forms.NumberInput(
                attrs={
                    'class':'form-control'
                }
            ),
        }