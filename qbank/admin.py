from django.contrib import admin
from .models import QuestionBank, QuestionOption, QuestionAnswerKey

# Register your models here.

admin.site.register(QuestionBank)
admin.site.register(QuestionOption)
admin.site.register(QuestionAnswerKey)