from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_ckeditor_5.fields import CKEditor5Field 
from easy_thumbnails.fields import ThumbnailerImageField
from django.utils.crypto import get_random_string
from user.models import User
from django.urls import reverse
# Create your models here.

from config.storage import PublicMediaStorage

class Newsletter(models.Model):
    phone_number = PhoneNumberField(verbose_name='شماره')

    def __str__(self):
        return str(self.phone_number).replace(' ','')

     
    class Meta:
        verbose_name = 'پیام نامه'
        verbose_name_plural = 'پیام نامه ها'

class QuestionAndAnswer(models.Model):
    question = models.TextField(verbose_name="سوال",  db_index=True)
    answer = models.TextField(verbose_name="جواب")
    order = models.PositiveIntegerField(verbose_name='ترتیب (توجه داشته باشید ۳ اول ترتیب در صفحه تیکت ها نمایش داده خواهد شد)',  db_index=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال یا غیر فعال")

    def __str__(self):
        return self.question
 
    class Meta:
        ordering = ['order']
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

def photo_path_upload_to(instance, filename):
    return f"team/avatar/{get_random_string(72)}-{filename}"

class Team(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام')
    work = models.CharField(max_length=255, verbose_name='سمت')
    phone_number = PhoneNumberField(verbose_name='شماره') 
    avatar = ThumbnailerImageField(verbose_name='عکس', upload_to=photo_path_upload_to, storage=PublicMediaStorage)
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    sort_number = models.IntegerField(default=0, verbose_name='ترتیب')

    def __str__(self):
        return str(self.phone_number).replace(' ','')

    class Meta:
        verbose_name = 'عضو تیم'
        verbose_name_plural = 'اعضای تیم'
        ordering = ['-sort_number']

def photo_path_upload_to(instance, filename):
    return f"site/logo/{get_random_string(72)}-{filename}"

class Site(models.Model):

    addr = models.CharField(max_length=255, verbose_name='ادرس')
    email = models.EmailField(verbose_name='ایمیل')

    name = models.CharField(max_length=255, verbose_name='نام')
    tag = models.CharField(max_length=255, verbose_name='تگ')
    work_hour = models.CharField(max_length=255, verbose_name='ساعات کاری')
    short_description = models.CharField(max_length=255, verbose_name='توضیحات کوتاه')
    copyright = models.CharField(max_length=255, verbose_name='متن کپی رایت', default='© 1405 سورنا . تمام حقوق محفوظ است.')

    # links 
    instagram_link = models.CharField(max_length=500, verbose_name='لینک حساب اینستاگرام', null=True, blank=True)
    telegram_link = models.CharField(max_length=500, verbose_name='لینک حساب تلگرام', null=True, blank=True)
    eitaa_link = models.CharField(max_length=500, verbose_name='لینک حساب ایتا', null=True, blank=True)

    # بلف زنی
    active_user = models.CharField(max_length=255, verbose_name='کاربر فعال')
    number_questions = models.CharField(max_length=255, verbose_name='تعداد سوالات')
    taken_exams = models.CharField(max_length=255, verbose_name='ازمون های برگذاری شده')
    user_happies = models.CharField(max_length=255, verbose_name='رضایت کاربران')

    force_to_login_with_otp = models.BooleanField(default=True, verbose_name='اجبار برای ورود با رمز یک بار مصرف')
    
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    active_blog = models.BooleanField(default=True, verbose_name='فعال بودن قسمت بلاگ ')
    active_qbank = models.BooleanField(default=True, verbose_name='فعال بودن قسمت بانک سوالات')
    

    logo = ThumbnailerImageField(verbose_name='لوگو', upload_to=photo_path_upload_to, storage=PublicMediaStorage)
    phone_number = PhoneNumberField(verbose_name='شماره') 
    description = CKEditor5Field(verbose_name="توضیحات ")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'تنظیمات'
        verbose_name_plural = 'تنظیمات'


# ====================== tickets =======================

class TicketProblemCategory(models.Model):
    order = models.PositiveIntegerField(default=1, verbose_name='ترتیب')
    name = models.CharField( max_length=255, verbose_name='نام  ')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-order']
        verbose_name = 'دسته بندی مشکل تیکت'
        verbose_name_plural = 'دسته بندی مشکلات تیکت ها'

class TicketProblemPlacement(models.Model):
    order = models.PositiveIntegerField(default=1, verbose_name='ترتیب')
    name = models.CharField( max_length=255, verbose_name='بخش مرتبط')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-order']
        verbose_name = 'بخش مرتبط مشکلات در تیکت'
        verbose_name_plural = 'بخش های مرتبط مشکلات در تیکت'


def photo_path_upload_to(instance, filename):
    return f"ticket-files/{get_random_string(100)}-{filename}"


class Ticket(models.Model):

    class TicketPriority(models.TextChoices):
        low = 'پایین','پایین'
        mid = 'متوسط','متوسط'
        high = 'بالا','بالا'
        huge = 'فوری','فوری'

    class TicketStatus(models.TextChoices):
        cancelled = 'کنسل شده','کنسل شده'
        fixed = 'حل شده','حل شده'
        awating_admin = 'در انتظار پاسخ ادمین','در انتظار پاسخ ادمین'
        awating_user = 'در انتظار پاسخ کاربر','در انتظار کاربر'
        
    name = models.CharField(max_length=500, verbose_name='موضوع',  db_index=True) 
    user =  models.ForeignKey(User, related_name='tickets', on_delete=models.PROTECT, verbose_name='درخواست دهنده',  db_index=True) 
    admin =  models.ForeignKey(User, related_name='tickets_admin', null=True, blank=True, on_delete=models.PROTECT, verbose_name='ادمین',  db_index=True) 

    problem =  models.ForeignKey(TicketProblemCategory, related_name='tickets', null=True, on_delete=models.PROTECT, verbose_name='دسته بندی مشکلات تیکت ها',  db_index=True) 
    placement =  models.ForeignKey(TicketProblemPlacement, related_name='tickets', null=True, on_delete=models.PROTECT, verbose_name='بخش های مرتبط مشکلات در تیکت',  db_index=True) 
    
    description = models.TextField(verbose_name="توضیحات ")
    file = models.FileField(verbose_name='پیوست', upload_to=photo_path_upload_to, null=True, blank=True, storage=PublicMediaStorage)
    priority = models.CharField(verbose_name='اهمیت', choices=TicketPriority, max_length=255)
    status = models.CharField(verbose_name='وضعیت', choices=TicketStatus, max_length=255)
    create_at = models.DateTimeField(verbose_name='زمان ارسال درخواست', auto_now_add=True)

    def get_absolute_url(self):
        return reverse("dashboard:ticket-chat", kwargs={"pk": self.pk})
    

    class Meta:
        ordering = ['-id']
        verbose_name ='تیکت '
        verbose_name_plural ='تیکت  ها'

    def __str__(self):
        return f'{self.name} - {self.user.PhoneNumber}'

class TicketChat(models.Model):
    ticket =  models.ForeignKey(Ticket, related_name='chats', on_delete=models.CASCADE, verbose_name='تیکت')
    create_at = models.DateTimeField(verbose_name='زمان ارسال پیام', auto_now_add=True)
    is_read_by_admin = models.BooleanField(verbose_name='خوانده شده توسط ادمین', default=False)
    is_read_by_user = models.BooleanField(verbose_name='خوانده شده توسط کاربر', default=False)
    is_admin_message = models.BooleanField(verbose_name='پیام ادمین', default=False)
    admin_message = CKEditor5Field(verbose_name="پیام", null=True, blank=True)
    user_message = models.TextField(verbose_name="پیام", null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name ='پیام تیکت  '
        verbose_name_plural ='پیام های تیکت'

    def __str__(self):
        return f'{self.id} - {self.ticket.name} - {self.ticket.user.PhoneNumber}'
