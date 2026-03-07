from django.db import models
from quiz.models import Quiz, LessionCategories
from user.models import User, MajorCategories, GradeCategories


# Create your models here.
class Report(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='کاربر', related_name='reports',)
    quiz = models.OneToOneField(Quiz, on_delete=models.PROTECT, verbose_name='ازمون', related_name='reports')

    grade =  models.ForeignKey(GradeCategories,null=True, blank=True, related_name='reports', on_delete=models.PROTECT, verbose_name='پایه') 
    major =  models.ForeignKey(MajorCategories,null=True, blank=True, related_name='reports', on_delete=models.PROTECT, verbose_name='رشته تحصیلی') 
    lession =  models.ForeignKey(LessionCategories,null=True, blank=True, related_name='reports', on_delete=models.PROTECT, verbose_name='درس') 

    score = models.PositiveIntegerField(verbose_name='نمره')
    percent = models.PositiveIntegerField(verbose_name='درصد')
    teraze = models.PositiveIntegerField(verbose_name='تراز')
    order = models.PositiveIntegerField(verbose_name='رتبه')

    def __str__(self):
        return f'{self.quiz.name} - {str(self.user.PhoneNumber).replace(" ", "")} - {self.teraze}'
    
    class Meta:
        ordering = ['order']
        verbose_name = 'کارنامه '
        verbose_name_plural = 'کارنامه ها'
        unique_together = ('quiz', 'user')

 

    