from django.db import models
from user.models import User
from quiz.models import Quiz
from blog.models import Blog
from qbank.models import QuestionBank

# Create your models here.

class UserFavorate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='favorate', db_index=True)
    quiz = models.ManyToManyField(Quiz, verbose_name='ازمون', related_name='favorate', db_index=True)
    blog = models.ManyToManyField(Blog, verbose_name='مقاله', related_name='favorate', db_index=True)
    qbank = models.ManyToManyField(QuestionBank, verbose_name='بانک سوال', related_name='favorate', db_index=True)

    class Meta:
        verbose_name='علاقه مندی'
        verbose_name_plural='علاقه مندی ها'

    def __str__(self):
        return f'{self.id} - {self.user.id} '