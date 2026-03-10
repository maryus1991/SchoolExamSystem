from django.db import models
from user.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.crypto import get_random_string
from user.models import GradeCategories, MajorCategories
from django.urls import reverse

class LessionCategories(models.Model):
    order = models.PositiveIntegerField(default=1, verbose_name='ترتیب')
    name = models.CharField( max_length=255, verbose_name='نام درس ')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = 'درس '
        verbose_name_plural = 'دروس'

    def get_absolute_url(self):
        return reverse("quiz:category-lession-list", kwargs={"lession_category_id": self.pk})

class Quiz(models.Model):
    student = models.ManyToManyField(User, null=True, blank=True, related_name='quiz_student', verbose_name='دانش اموز')
    sanatorium = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='quiz_sanatorium', verbose_name='مصحح')
    name = models.CharField(verbose_name='عنوان', max_length=255 )
    section = models.CharField(verbose_name='مبحث', max_length=255 )

    grade =  models.ForeignKey(GradeCategories, related_name='quiz', on_delete=models.PROTECT, verbose_name='پایه') 
    major =  models.ForeignKey(MajorCategories, related_name='quiz', on_delete=models.PROTECT, verbose_name='رشته تحصیلی') 
    lession =  models.ForeignKey(LessionCategories, related_name='quiz', on_delete=models.PROTECT, verbose_name='درس') 

    province =  models.CharField(max_length=255, verbose_name=' نام استان محل برگذاری') 
    city =  models.CharField(max_length=255, verbose_name='نام شهر محل برگذاری') 
    type_of_quiz =  models.CharField(max_length=255, verbose_name='محل و نحوه برگذاری')
    description = CKEditor5Field()
    price = models.PositiveBigIntegerField(default=0, verbose_name='هزینه')
    time_minutes = models.PositiveIntegerField(default=0, verbose_name='(دقیقه) تایمر')

    create_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')
    start_at = models.DateTimeField(verbose_name='زمان برگذاری')
    stop_at = models.DateTimeField(verbose_name='زمان پایان')
    last_enter = models.DateTimeField(verbose_name='اخرین زمان ورود')
    finished_at = models.DateTimeField(verbose_name='زمان تمام شدن توسط کاربر', null=True, blank=True)
    corrected_at = models.DateTimeField(verbose_name='زمان تصحیح', null=True, blank=True)

    max_score = models.PositiveSmallIntegerField(verbose_name='حداکثر نمره', default=100)
    score = models.PositiveSmallIntegerField(verbose_name='ضریب', default=1)
    capacity = models.PositiveSmallIntegerField(verbose_name='ظرفیت', default=1)
    filled_capacity = models.PositiveSmallIntegerField(verbose_name=' ظرفیت پر شده', default=0)
    
    class QuizStatus(models.TextChoices):
        
        ALL_STATUS = 'همه وضعیت ها ', 'همه وضعیت ها '
        WAITING_START = 'در انتظار شروع', 'در انتظار شروع'
        STARTED = 'شروع شده', 'شروع شده'
        WAITING_END = 'در انتظار پایان', 'در انتظار پایان'
        FINISHED = 'پایان یافته', 'پایان یافته'
        WAITING_CORRECTION = 'در انتظار تصحیح', 'در انتظار تصحیح'
        CORRECTED = 'تصحیح شده', 'تصحیح شده'
        RESULTS_PUBLISHED = 'اعلام نتایج', 'اعلام نتایج'
        DEACTIVATED = 'غیرفعال', 'غیرفعال'
        CANCELED = 'کنسل شده', 'کنسل شده'

    status = models.CharField(verbose_name='وضعیت', choices=QuizStatus, default=QuizStatus.WAITING_START, max_length=55)
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_online = models.BooleanField(default=True, verbose_name='انلاین')
    allow_return_to_questions = models.BooleanField(default=True, verbose_name='برگشتن به عقب')
    change_the_order = models.BooleanField(default=True, verbose_name=' عوض کردن ترتیب سوالات')
    allow_to_edit_the_answered_questions = models.BooleanField(default=True, verbose_name='امکان ویرایش سوالات پاسخ داده شده')
    have_negetive_score = models.BooleanField(default=True, verbose_name='دارای نمره منفی')

    class Meta:
        verbose_name = 'ازمون'
        verbose_name_plural = 'ازمون ها'
 
            

    def __str__(self):
        return f"{self.id} - {self.name}"

    def get_absolute_url(self):
        return reverse("quiz:detail", kwargs={"pk": self.pk})

def photo_path_upload_to(instance, filename):
    return f"questions/{get_random_string(100)}-{filename}"


class UserQuizDetail(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.PROTECT, related_name='detail', verbose_name='آزمون')
    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='quiz_detail', verbose_name='دانش اموز')
    finished_at = models.DateTimeField(verbose_name='زمان تمام شدن توسط کاربر', null=True, blank=True)
    out_of_page = models.PositiveSmallIntegerField(verbose_name='خروج از صفحه', default=0)
    score = models.PositiveSmallIntegerField(verbose_name='نمره کل', default=0)

    class Meta:
        verbose_name = 'جزییات ازمون برای دانش اموزان'
        verbose_name_plural = 'جزییات ازمون ها برای دانش اموزان'
 
            

    def __str__(self):
        return f"{self.id} - {self.quiz.name} - {self.student.PhoneNumber}"


class Question(models.Model):

    class TypeOfQuestions(models.TextChoices):
        MULTIPLE_CHOICE = 'تستی چهارگزینه‌ای', 'تستی چهارگزینه‌ای'
        SHORT_ANSWER = 'پاسخ کوتاه', 'پاسخ کوتاه'
        LONG_ANSWER = 'پاسخ تشریحی', 'پاسخ تشریحی'
        IMAGE_BASED = 'مبتنی بر تصویر', 'مبتنی بر تصویر'
        PDF_BASED = 'سوال از فایل PDF', 'سوال از فایل PDF'

    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='questions', verbose_name='آزمون')
    type_of_question = models.CharField( max_length=100, choices=TypeOfQuestions.choices, verbose_name='نوع سوال')
    name = models.CharField( max_length=255, verbose_name='عنوان سوال')
    description = CKEditor5Field( blank=True, null=True, verbose_name='متن سوال')
    image = models.ImageField( upload_to=photo_path_upload_to, blank=True, null=True, verbose_name='تصویر سوال' )
    pdf_file = models.FileField( upload_to=photo_path_upload_to, blank=True, null=True, verbose_name='فایل PDF سوال' )

    score = models.PositiveIntegerField( default=1, verbose_name='نمره سوال')

    order = models.PositiveIntegerField( default=1, verbose_name='ترتیب نمایش' )
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True )

    class Meta:
        ordering = ['id']
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'

    def __str__(self):
        return f"{self.quiz} - {self.name}"


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options', verbose_name='سوال')
    text = models.CharField(max_length=500, verbose_name='متن گزینه')
    is_correct = models.BooleanField(default=False, verbose_name='گزینه صحیح')
    order = models.PositiveIntegerField(default=1, verbose_name='ترتیب')

    class Meta:
        ordering = ['order']
        verbose_name = ' گزینه سوال تست'
        verbose_name_plural = 'گزینه‌ها سوالات تستی'

    def __str__(self):
        return f"{self.question.name} - {self.text}"
    

def photo_path_upload_to(instance, filename):
    return f"questions/{get_random_string(100)}-{filename}"


class QuestionAnswerKey(models.Model):
    class TypeOfAnswer(models.TextChoices):
        TEXT_BASED = 'پاسخ تشریحی', 'پاسخ تشریحی'
        IMAGE_BASED = 'پاسخ تصویری', 'پاسخ تصویری'
        PDF_BASED = 'پاسخ PDF', 'پاسخ PDF'

    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='answer_key', verbose_name='سوال')
    type_of_answer = models.CharField(max_length=50, choices=TypeOfAnswer.choices, verbose_name='نوع پاسخ صحیح')
    description = CKEditor5Field(blank=True, null=True, verbose_name='متن پاسخ')
    image = models.ImageField(upload_to=photo_path_upload_to, blank=True, null=True, verbose_name='تصویر پاسخ')
    pdf_file = models.FileField(upload_to=photo_path_upload_to, blank=True,null=True, verbose_name='فایل PDF پاسخ')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'پاسخ صحیح (ادمین)'
        verbose_name_plural = 'پاسخ‌های صحیح (ادمین)'

    def __str__(self):
        return f"پاسخ صحیح - {self.question.name}"  
    

    
def photo_path_upload_to(instance, filename):
    return f"questions/{get_random_string(100)}-{filename}"



class StudentAnswer(models.Model):
    class TypeOfAnswer(models.TextChoices):
        OPTION = 'انتخاب گزینه', 'انتخاب گزینه'
        TEXT_BASED = 'پاسخ متنی', 'پاسخ متنی'
        IMAGE_BASED = 'پاسخ تصویری', 'پاسخ تصویری'
        PDF_BASED = 'پاسخ PDF', 'پاسخ PDF'
        SKIPPED = 'رد شده', 'رد شده'
        NOT_ANSWERD = 'جواب داده نشده', 'جواب داده نشده'

    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='student_answers', verbose_name='آزمون')
    student = models.ForeignKey(User, on_delete=models.CASCADE,related_name='answers', verbose_name='دانش‌آموز')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='student_answers', null=True, blank=True , verbose_name='سوال')
    
    type_of_answer = models.CharField(max_length=50,choices=TypeOfAnswer.choices,verbose_name='نوع پاسخ', default=TypeOfAnswer.NOT_ANSWERD)
    selected_option = models.ForeignKey(QuestionOption,on_delete=models.PROTECT ,null=True,blank=True,verbose_name='گزینه انتخاب‌شده')
    description = models.TextField(blank=True, null=True,verbose_name='متن پاسخ' )
    image = models.ImageField(upload_to=photo_path_upload_to, blank=True, null=True, verbose_name='تصویر پاسخ')
    pdf_file = models.FileField(upload_to=photo_path_upload_to, blank=True, null=True, verbose_name='فایل PDF پاسخ')
    is_skipped = models.BooleanField(default=False, verbose_name='رد شده' )

    class TypeOfCorrect(models.TextChoices):
        not_corrected = 'تصحیح نشده', 'تصحیح نشده'
        wrong = 'کاملا اشتباه', 'کاملا اشتباه'
        weak = 'نیاز به تلاش بیشتر', 'نیاز به تلاش بیشتر'
        average = 'قابل قبول', 'قابل قبول'
        good = 'نسبتا درست', 'نسبتا درست'
        excellent = 'کاملا درست', 'کاملا درست'

    corrected = models.CharField(max_length=100, choices=TypeOfCorrect.choices,verbose_name='کیفیت جواب', default=TypeOfCorrect.not_corrected ,)
    corrected_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='corrected_answers', verbose_name='تصحیح‌کننده')
    corrected_at = models.DateTimeField(null=True, blank=True)
    satantorium_message = CKEditor5Field(blank=True, null=True, verbose_name='نظر مصصح' )

    score = models.FloatField(default=0, verbose_name='نمره داده شده')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['question__pk']
        verbose_name = 'پاسخ دانش‌آموز'
        verbose_name_plural = 'پاسخ‌های دانش‌آموزان'
        unique_together = ('student', 'question')

    def __str__(self):
        return f"{self.id}"
    

class QuizView(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="views")
    ip = models.GenericIPAddressField()
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip
    
    class Meta:
        verbose_name = 'بازدید'
        verbose_name_plural = 'بازدید ها '