from django.db import models
from user.models import User
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Quiz(models.Model):
    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='quiz_student', verbose_name='دانش اموز')
    sanatorium = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='quiz_sanatorium', verbose_name='مصحح')
    name = models.CharField(verbose_name='عنوان', max_length=255 )
    grade =  models.CharField(max_length=255, verbose_name='پایه') 
    major =  models.CharField(max_length=255, verbose_name='رشته تحصیلی')  
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
    max_score = models.PositiveSmallIntegerField(verbose_name='حداکثر نمره', default=100)
    score = models.PositiveSmallIntegerField(verbose_name='ضریب', default=1)
    
    class QuizStatus(models.TextChoices):
        
        DEACTIVATED = 'DEACTIVATED', 'غیرفعال'
        CANCELED = 'CANCELED', 'کنسل شده'
        WAITING_START = 'WAITING_START', 'در انتظار شروع'
        STARTED = 'STARTED', 'شروع شده'
        WAITING_END = 'WAITING_END', 'در انتظار پایان'
        FINISHED = 'FINISHED', 'پایان یافته'
        WAITING_CORRECTION = 'WAITING_CORRECTION', 'در انتظار تصحیح'
        CORRECTED = 'CORRECTED', 'تصحیح شده'
        RESULTS_PUBLISHED = 'RESULTS_PUBLISHED', 'اعلام نتایج'

    status = models.CharField(verbose_name='وضعیت', choices=QuizStatus, default=QuizStatus.WAITING_START, max_length=55)

    class Meta:
        verbose_name = 'ازمون'
        verbose_name_plural = 'ازمون ها'

    def __str__(self):
        return f"{self.id} - {self.name}"

class Question(models.Model):

    class TypeOfQuestions(models.TextChoices):
        MULTIPLE_CHOICE = 'MULTIPLE_CHOICE', 'تستی چهارگزینه‌ای'
        TRUE_FALSE = 'TRUE_FALSE', 'درست / نادرست'
        SHORT_ANSWER = 'SHORT_ANSWER', 'پاسخ کوتاه'
        LONG_ANSWER = 'LONG_ANSWER', 'پاسخ تشریحی'
        IMAGE_BASED = 'IMAGE_BASED', 'مبتنی بر تصویر'
        PDF_BASED = 'PDF_BASED', 'سوال از فایل PDF'

    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='questions', verbose_name='آزمون')
    type_of_question = models.CharField( max_length=50, choices=TypeOfQuestions.choices, verbose_name='نوع سوال')
    name = models.CharField( max_length=255, verbose_name='عنوان سوال')
    description = CKEditor5Field( blank=True, null=True, verbose_name='متن سوال')
    image = models.ImageField( upload_to='questions/images/', blank=True, null=True, verbose_name='تصویر سوال' )
    pdf_file = models.FileField( upload_to='questions/pdfs/', blank=True, null=True, verbose_name='فایل PDF سوال' )
    score = models.PositiveIntegerField( default=1, verbose_name='نمره سوال')
    order = models.PositiveIntegerField( default=1, verbose_name='ترتیب نمایش' )
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True )

    class Meta:
        ordering = ['order']
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'

    def __str__(self):
        return f"{self.quiz} - {self.title}"

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
        return f"{self.question.title} - {self.text}"
    


class QuestionAnswerKey(models.Model):
    class TypeOfAnswer(models.TextChoices):
        TEXT_BASED = 'TEXT_BASED', 'پاسخ تشریحی'
        IMAGE_BASED = 'IMAGE_BASED', 'پاسخ تصویری'
        PDF_BASED = 'PDF_BASED', 'پاسخ PDF'

    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='answer_key', verbose_name='سوال')
    type_of_answer = models.CharField(max_length=50, choices=TypeOfAnswer.choices, verbose_name='نوع پاسخ صحیح')
    description = CKEditor5Field(blank=True, null=True, verbose_name='متن پاسخ')
    image = models.ImageField(upload_to='answers/admin/images/', blank=True, null=True, verbose_name='تصویر پاسخ')
    pdf_file = models.FileField(upload_to='answers/admin/pdfs/',blank=True,null=True, verbose_name='فایل PDF پاسخ')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'پاسخ صحیح (ادمین)'
        verbose_name_plural = 'پاسخ‌های صحیح (ادمین)'

    def __str__(self):
        return f"پاسخ صحیح - {self.question.title}"
    

class StudentAnswer(models.Model):
    class TypeOfAnswer(models.TextChoices):
        TEXT_BASED = 'TEXT_BASED', 'پاسخ متنی'
        IMAGE_BASED = 'IMAGE_BASED', 'پاسخ تصویری'
        PDF_BASED = 'PDF_BASED', 'پاسخ PDF'
        OPTION = 'OPTION', 'انتخاب گزینه'

    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='student_answers', verbose_name='آزمون')
    student = models.ForeignKey(User, on_delete=models.CASCADE,related_name='answers', verbose_name='دانش‌آموز')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='student_answers', verbose_name='سوال')
    type_of_answer = models.CharField(max_length=50,choices=TypeOfAnswer.choices,verbose_name='نوع پاسخ')
    selected_option = models.ForeignKey(QuestionOption,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='گزینه انتخاب‌شده')
    description = models.TextField(blank=True, null=True,verbose_name='متن پاسخ' )
    image = models.ImageField(upload_to='answers/student/images/', blank=True, null=True, verbose_name='تصویر پاسخ')
    pdf_file = models.FileField(upload_to='answers/student/pdfs/', blank=True, null=True, verbose_name='فایل PDF پاسخ')
    score = models.FloatField(default=0, verbose_name='نمره داده شده')
    is_correct = models.BooleanField(default=False, verbose_name='صحیح است؟' )
    corrected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='corrected_answers', verbose_name='تصحیح‌کننده')
    corrected_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'پاسخ دانش‌آموز'
        verbose_name_plural = 'پاسخ‌های دانش‌آموزان'
        unique_together = ('student', 'question')

    def __str__(self):
        return f"{self.id}"