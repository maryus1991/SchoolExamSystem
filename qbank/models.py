from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.crypto import get_random_string
from django.urls import reverse
from quiz.models import LessionCategories


class QuestionLessonCategory(models.Model):
    order = models.PositiveIntegerField(default=1, verbose_name='ترتیب')
    name = models.CharField( max_length=255, verbose_name='نام دسته')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = 'دسته'
        verbose_name_plural = 'دسته ها'


    def get_absolute_url(self):
        return reverse("qbank:list-by-category", kwargs={"category_id": self.pk})
    

class QuestionPossible(models.Model):
    name = models.CharField( max_length=255, verbose_name='نام سطح')
    order = models.PositiveIntegerField(default=1, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')


    def __str__(self):
        return self.name


    class Meta:
        ordering = ['-order']
        verbose_name = 'سطح'
        verbose_name_plural = 'سطوح'

def photo_path_upload_to(instance, filename):
    return f"questions/{get_random_string(100)}-{filename}"



class QuestionBank(models.Model):
    class TypeOfQuestions(models.TextChoices):
        ALL = 'همه', 'همه'
        MULTIPLE_CHOICE = 'تستی چهارگزینه‌ای', 'تستی چهارگزینه‌ای'
        TRUE_FALSE = 'درست / نادرست', 'درست / نادرست'
        SHORT_ANSWER = 'پاسخ کوتاه ', 'پاسخ کوتاه '
        LONG_ANSWER = 'پاسخ تشریحی', 'پاسخ تشریحی'
        IMAGE_BASED = 'مبتنی بر تصویر', 'مبتنی بر تصویر'
        PDF_BASED = 'سوال از فایل PDF', 'سوال از فایل PDF'

    possible = models.ForeignKey(QuestionPossible, related_name='questions', on_delete=models.CASCADE, verbose_name='سطح' ,db_index=True)
    category = models.ForeignKey(LessionCategories, related_name='questions', on_delete=models.CASCADE, verbose_name='درس' ,db_index=True)
    type_of_question = models.CharField( max_length=50, choices=TypeOfQuestions.choices, verbose_name='نوع سوال')
    name = models.CharField( max_length=255, verbose_name='عنوان سوال' ,db_index=True)
    lesson = models.CharField( max_length=255, verbose_name='مبحث')
    description = CKEditor5Field( blank=True, null=True, verbose_name='متن سوال')
    image = models.ImageField( upload_to=photo_path_upload_to, blank=True, null=True, verbose_name='تصویر سوال' )
    pdf_file = models.FileField( upload_to=photo_path_upload_to, blank=True, null=True, verbose_name='فایل PDF سوال' )
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    has_options = models.BooleanField(default=False, verbose_name='دارای گزینه های دیگر')
    created_at = models.DateTimeField(auto_now_add=True )
    order = models.PositiveIntegerField(default=1, verbose_name='ترتیب' )
    solving_time = models.PositiveIntegerField(default=1, verbose_name='زمان پیشنهادی حل به دقیقه')

    class Meta:
        ordering = ['-order']
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'

    def __str__(self):
        return f"{self.id} - {self.name}"
    
    def get_absolute_url(self):
        return reverse("qbank:detail", kwargs={"pk": self.pk})
    

class QuestionOption(models.Model):
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, related_name='options', verbose_name='سوال', db_index=True)
    text = models.CharField(max_length=500, verbose_name='متن گزینه')
    is_correct = models.BooleanField(default=False, verbose_name='گزینه صحیح')
    order = models.PositiveIntegerField(default=1, verbose_name='ترتیب')

    class Meta:
        ordering = ['-order']
        verbose_name = ' گزینه سوال تست'
        verbose_name_plural = 'گزینه‌ها سوالات تستی'

    def __str__(self):
        return f"{self.question.name} - {self.text}"
    
class QuestionAnswerKey(models.Model):
    class TypeOfAnswer(models.TextChoices):
        TEXT_BASED = 'پاسخ تشریحی', 'پاسخ تشریحی'
        IMAGE_BASED = 'پاسخ تصویری', 'پاسخ تصویری'
        PDF_BASED = 'پاسخ PDF', 'پاسخ PDF'

    question = models.OneToOneField(QuestionBank, on_delete=models.CASCADE, related_name='answer_key', verbose_name='سوال', db_index=True)
    type_of_answer = models.CharField(max_length=50, choices=TypeOfAnswer.choices, verbose_name='نوع پاسخ صحیح')
    description = CKEditor5Field(blank=True, null=True, verbose_name='متن پاسخ')
    image = models.ImageField(upload_to=photo_path_upload_to, blank=True, null=True, verbose_name='تصویر پاسخ')
    pdf_file = models.FileField(upload_to=photo_path_upload_to,blank=True,null=True, verbose_name='فایل PDF پاسخ')
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"پاسخ صحیح - {self.question.name}"
    


class QuestionView(models.Model):
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, related_name="views", db_index=True)
    ip = models.GenericIPAddressField()
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'بازدید سوال'
        verbose_name_plural = 'بازدید های سوالات'

    def __str__(self):
        return self.ip