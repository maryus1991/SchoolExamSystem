from django.contrib import admin
from .models import (
    LessionCategories, 
    Quiz, 
    QuestionOption, 
    Question, 
    QuestionAnswerKey, 
    QuizView,
    StudentAnswer,
)

admin.site.register(LessionCategories)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(QuestionAnswerKey)
admin.site.register(StudentAnswer)
admin.site.register(QuizView) 