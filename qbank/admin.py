from django.contrib import admin
from .models import QuestionBank, QuestionOption, QuestionAnswerKey, QuestionView, QuestionPossible, QuestionLessonCategory

# Register your models here.

admin.site.register(QuestionBank)
admin.site.register(QuestionOption)
admin.site.register(QuestionAnswerKey)
admin.site.register(QuestionView)
admin.site.register(QuestionLessonCategory)
admin.site.register(QuestionPossible)