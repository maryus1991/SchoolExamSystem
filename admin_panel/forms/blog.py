from django import forms
from blog.models import Blog
from django.core.validators import FileExtensionValidator
from django_ckeditor_5.fields import CKEditor5Widget

class BlogModelForm(forms.ModelForm):

    image = forms.ImageField(
        required=True,
        label='عکس',
        widget=forms.FileInput(
            attrs={
                'class':'form-control',   
            }
        ),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "webp", "heic"]
            )
        ],
    )

    content = CKEditor5Widget(
            attrs={
                'placeholder':'بدنه',
                'class':'form-control'
            }
        ),

    class Meta:
        model = Blog
        fields = [
            'content', 
            'image', 
            'title', 
            'category', 
            'short_content', 
            'time_to_read_minutes',
            'sort_number'
        ]

        widgets={
            'title': forms.TextInput(
                attrs={
                    'placeholder':'عنوان',
                    'class':'form-control'
                }
            ),

            'category': forms.TextInput(
                attrs={
                    'placeholder':'نام دسته',
                    'class':'form-control'
                }
            ),
            'sort_number': forms.NumberInput(
                attrs={
                    'placeholder':'عدد ترتیبی',
                    'class':'form-control'
                }
            ),
            'short_content': forms.Textarea(
                attrs={
                    'placeholder':'توضیحات کوتاه',
                    'class':'form-control'
                }
            ),
            'time_to_read_minutes': forms.NumberInput(
                attrs={
                    'placeholder':'مدت زمان خواندن (دقیقه)',
                    'class':'form-control'
                }
            ),
        }