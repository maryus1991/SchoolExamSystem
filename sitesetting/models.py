from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_ckeditor_5.fields import CKEditor5Field 
from easy_thumbnails.fields import ThumbnailerImageField
from django.utils.crypto import get_random_string

# Create your models here.


class Newsletter(models.Model):
    phone_number = PhoneNumberField(verbose_name='شماره')

    def __str__(self):
        return str(self.phone_number).replace(' ','')

     
    class Meta:
        verbose_name = 'پیام نامه'
        verbose_name_plural = 'پیام نامه ها'

class QuestionAndAnswer(models.Model):
    question = models.TextField(verbose_name="سوال")
    answer = models.TextField(verbose_name="جواب")

    is_active = models.BooleanField(default=True, verbose_name="فعال یا غیر فعال")

    def __str__(self):
        return self.question
 
    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'


class ContactUs(models.Model):
    subject = models.CharField(max_length=100, verbose_name='موضوع')
    name = models.CharField(max_length=100, verbose_name='نام')

    phone = PhoneNumberField(verbose_name='شماره')
    message = models.TextField(verbose_name='پیام')
    admin_read = models.BooleanField(default=False, verbose_name='خوانده شده توسط ادمین')

    def __str__(self):
        return f"{self.subject} - {self.name} - {self.phone}"

 

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'تماس با ما'

class SiteLaw(models.Model):
    name = models.CharField(verbose_name="نام قانون", max_length=250)
    description = CKEditor5Field (verbose_name="توضیحات ")
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    sort_number = models.IntegerField(default=0, verbose_name='ترتیب')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'قانون'
        verbose_name_plural = 'قوانین'
        ordering = ['-sort_number']



def photo_path_upload_to(*args, **kwargs):
    return f"team/avatar/{get_random_string(72)}"


class Team(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام')
    work = models.CharField(max_length=255, verbose_name='سمت')
    phone_number = PhoneNumberField(verbose_name='شماره') 
    avatar = ThumbnailerImageField(verbose_name='عکس', upload_to=photo_path_upload_to)
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    sort_number = models.IntegerField(default=0, verbose_name='ترتیب')



    def __str__(self):
        return str(self.phone_number).replace(' ','')

    class Meta:
        verbose_name = 'عضو تیم'
        verbose_name_plural = 'اعضای تیم'
        ordering = ['-sort_number']



def photo_path_upload_to(*args, **kwargs):
    return f"site/logo/{get_random_string(72)}"


class Site(models.Model):
    logo = ThumbnailerImageField(verbose_name='لوگو', upload_to=photo_path_upload_to)
    name = models.CharField(max_length=255, verbose_name='نام')
    addr = models.CharField(max_length=255, verbose_name='ادرس')
    work_hour = models.CharField(max_length=255, verbose_name='ساعات کاری')
    phone_number = PhoneNumberField(verbose_name='شماره') 
    email = models.EmailField(verbose_name='ایمیل')
    short_description = models.CharField(max_length=255, verbose_name='توضیحات کوتاه')
    description = CKEditor5Field(verbose_name="توضیحات ")
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')

    active_user = models.CharField(max_length=255, verbose_name='کاربر فعال')
    number_questions = models.CharField(max_length=255, verbose_name='تعداد سوالات')
    taken_exams = models.CharField(max_length=255, verbose_name='ازمون های برگذاری شده')
    user_happies = models.CharField(max_length=255, verbose_name='رضایت کاربران')

    force_to_login_with_otp = models.BooleanField(default=True, verbose_name='اجبار برای ورود با رمز یک بار مصرف')
    

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'تنظیمات'
        verbose_name_plural = 'تنظیمات'
