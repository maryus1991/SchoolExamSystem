from django import forms
from quiz.models import Quiz, Question, QuestionOption, QuestionAnswerKey, GradeCategories, MajorCategories, LessionCategories
from . import BaseForm
from django_ckeditor_5.widgets import CKEditor5Widget
from django.core.validators import FileExtensionValidator

class QuizModelForm(BaseForm, forms.ModelForm):

    status = forms.ChoiceField(
        required=True,
        label="وضعیت",
        
        choices=Quiz.QuizStatus,
        widget=forms.Select(
            attrs={
                'class':'form-control',
                'placeholder':'وضعیت'
            }
        )
    )

    grade = forms.ModelChoiceField(
        required=True,
        label='پایه',
        empty_label='پایه',
        queryset=GradeCategories.objects.filter(is_active=True).all(),
        widget=forms.Select(
            attrs={
                'class':'form-control',
                'placeholder':'پایه'
            }
        )
    )
    major = forms.ModelChoiceField(
        required=True,
        label='رشته',
        empty_label='رشته',
        queryset=MajorCategories.objects.filter(is_active=True).all(),
        widget=forms.Select(
            attrs={
                'class':'form-control',
                'placeholder':'درس'
            }
        )
    )
    lession = forms.ModelChoiceField(
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
    description = forms.CharField(
        required=False,
        label='توضیحات',
        widget=CKEditor5Widget()
    )

    class Meta:
        model = Quiz
        exclude = ['id']

class QuestionModelForm(BaseForm, forms.ModelForm):

    description = forms.CharField(
        required=False,
        label='توضیحات',
        widget=CKEditor5Widget()
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

    type_of_question = forms.ChoiceField(
        required=True,
        label="نوع سوال",
        
        choices=Question.TypeOfQuestions,
        widget=forms.Select(
            attrs={
                'class':'form-control',
                'placeholder':'نوع سوال'
            }
        )
    )

    class Meta:
        model = Question
        exclude=['quiz', 'created_at']

class QuestionAnwerKeyModelForm(BaseForm, forms.ModelForm):

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
            'pdf_file',
        ]
 
class QuestionOptionsModelForm(BaseForm, forms.ModelForm):
    class Meta:
        model= QuestionOption
        fields = ['text' ,'is_correct' ,'order']
 