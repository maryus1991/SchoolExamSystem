from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class QuestionBank(models.Model):

    class TypeOfQuestions(models.TextChoices):
        MULTIPLE_CHOICE = 'MULTIPLE_CHOICE', 'تستی چهارگزینه‌ای'
        TRUE_FALSE = 'TRUE_FALSE', 'درست / نادرست'
        SHORT_ANSWER = 'SHORT_ANSWER', 'پاسخ کوتاه'
        LONG_ANSWER = 'LONG_ANSWER', 'پاسخ تشریحی'
        IMAGE_BASED = 'IMAGE_BASED', 'مبتنی بر تصویر'
        PDF_BASED = 'PDF_BASED', 'سوال از فایل PDF'

    type_of_question = models.CharField( max_length=50, choices=TypeOfQuestions.choices, verbose_name='نوع سوال')
    name = models.CharField( max_length=255, verbose_name='عنوان سوال')
    description = CKEditor5Field( blank=True, null=True, verbose_name='متن سوال')
    image = models.ImageField( upload_to='questions-bank/images/', blank=True, null=True, verbose_name='تصویر سوال' )
    pdf_file = models.FileField( upload_to='questions-bank/pdfs/', blank=True, null=True, verbose_name='فایل PDF سوال' )
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True )
    order = models.PositiveIntegerField(default=1, verbose_name='ترتیب')

    class Meta:
        ordering = ['order']
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'

    def __str__(self):
        return f"{self.quiz} - {self.title}"

class QuestionOption(models.Model):
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, related_name='options', verbose_name='سوال')
    text = models.CharField(max_length=500, verbose_name='متن گزینه')
    is_correct = models.BooleanField(default=False, verbose_name='گزینه صحیح')
    order = models.PositiveIntegerField(default=1, verbose_name='ترتیب')

    class Meta:
        ordering = ['order']
        verbose_name = ' گزینه سوال تست'
        verbose_name_plural = 'گزینه‌ها سوالات تستی'

    def __str__(self):
        return f"{self.question.title} - {self.text}"
    
class QuestionAnswerKey(models.Model):
    class TypeOfAnswer(models.TextChoices):
        TEXT_BASED = 'TEXT_BASED', 'پاسخ تشریحی'
        IMAGE_BASED = 'IMAGE_BASED', 'پاسخ تصویری'
        PDF_BASED = 'PDF_BASED', 'پاسخ PDF'

    question = models.OneToOneField(QuestionBank, on_delete=models.CASCADE, related_name='answer_key', verbose_name='سوال')
    type_of_answer = models.CharField(max_length=50, choices=TypeOfAnswer.choices, verbose_name='نوع پاسخ صحیح')
    description = CKEditor5Field(blank=True, null=True, verbose_name='متن پاسخ')
    image = models.ImageField(upload_to='answers/qbank/admin/images/', blank=True, null=True, verbose_name='تصویر پاسخ')
    pdf_file = models.FileField(upload_to='answers/qbank/admin/pdfs/',blank=True,null=True, verbose_name='فایل PDF پاسخ')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'پاسخ صحیح (ادمین)'
        verbose_name_plural = 'پاسخ‌های صحیح (ادمین)'

    def __str__(self):
        return f"پاسخ صحیح - {self.question.title}"
    