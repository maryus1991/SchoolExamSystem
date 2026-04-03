from django import forms
from django.core.validators import FileExtensionValidator, MaxLengthValidator
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
 
MAX_SIZE_PDF = 100 * 1024 * 1024 
MAX_SIZE_IMG = 10 * 1024 * 1024 

class AnswerForm(forms.Form):
    file = forms.FileField(
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
                allowed_extensions=[ 'pdf', 'jpg', 'jpeg', 'png', 'webp', 'heic']
            ),

        ],
    )
    image = forms.ImageField(
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
                allowed_extensions=[ 'jpg', 'jpeg', 'png', 'webp', 'heic']
            )
        ],
    )

    answer = forms.CharField(
        required=False,
        label='توضیحات',
        widget=forms.Textarea()
    )

    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        if file:
            
            if file.size > MAX_SIZE_PDF and file.content_type in ['application/pdf']:
                raise forms.ValidationError(
                    f'حجم فایل نباید بیشتر از {MAX_SIZE_PDF / 1024 / 1024}MB باشد'
                )
            elif file.size > MAX_SIZE_IMG and file.content_type not in ['application/pdf']:
                raise forms.ValidationError(
                    f'حجم عکس نباید بیشتر از {MAX_SIZE_IMG / 1024 / 1024}MB باشد'
                )
            
        return file

    def clean_image(self):
        file = self.cleaned_data.get('image')
        
        if file:
            
 
            if file.size > MAX_SIZE_IMG:
                raise forms.ValidationError(
                    f'حجم عکس نباید بیشتر از {MAX_SIZE_IMG / 1024 / 1024}MB باشد'
                )
            
        return file