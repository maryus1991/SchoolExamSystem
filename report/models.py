from django.db import models
from quiz.models import Quiz, LessionCategories
from user.models import User, MajorCategories, GradeCategories


# Create your models here.
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='کاربر', related_name='reports',)
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT, verbose_name='ازمون', related_name='reports')
    grade =  models.ForeignKey(GradeCategories,null=True, blank=True, related_name='reports', on_delete=models.PROTECT, verbose_name='پایه') 
    major =  models.ForeignKey(MajorCategories,null=True, blank=True, related_name='reports', on_delete=models.PROTECT, verbose_name='رشته تحصیلی') 
    lession =  models.ForeignKey(LessionCategories,null=True, blank=True, related_name='reports', on_delete=models.PROTECT, verbose_name='درس') 
    score = models.PositiveIntegerField(verbose_name='نمره')
    percent = models.PositiveIntegerField(verbose_name='درصد')

    teraze = models.PositiveIntegerField(verbose_name='تراز', default=0)
    order = models.PositiveIntegerField(verbose_name='رتبه', default=0)

    class ReportStatus(models.TextChoices):
        not_corrected = 'تصحیح نشده', 'تصحیح نشده'
        weak = 'نیاز به تلاش بیشتر', 'نیاز به تلاش بیشتر'
        average = 'متوسط', 'متوسط'
        good = 'خوب', 'خوب'
        excellent = 'عالی', 'عالی'

    status = models.CharField(max_length=100, choices=ReportStatus.choices, verbose_name='وضعیت عملکردی', default=ReportStatus.not_corrected)

    def __str__(self):
        return f'{self.quiz.name} - {str(self.user.PhoneNumber).replace(" ", "")} - {self.teraze} - {self.percent} - {self.score} - {self.status}'
    
    class Meta:
        ordering = ['order']
        verbose_name = 'کارنامه '
        verbose_name_plural = 'کارنامه ها'
        unique_together = ('quiz', 'user')

 

    