from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import timedelta, now
from random import randint
from .managers import UserManager
from config.settings import OTP_EXPIRATIONS_SECONDS, LOGIN_TEMP
from django.urls import reverse
from django.utils.crypto import get_random_string

# Create your models here.

class GradeCategories(models.Model):
    order = models.PositiveIntegerField(default=1, verbose_name='ترتیب')
    name = models.CharField( max_length=255, verbose_name='نام پایه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = 'پایه'
        verbose_name_plural = 'پایه ها'

    def get_absolute_url(self):
        return reverse("quiz:category-grade-list", kwargs={"grade_category_id": self.pk})
    


class MajorCategories(models.Model):
    order = models.PositiveIntegerField(default=1, verbose_name='ترتیب')
    name = models.CharField( max_length=255, verbose_name='نام رشته')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = 'رشته '
        verbose_name_plural = 'رشته ها'


    def get_absolute_url(self):
        return reverse("quiz:category-major-list", kwargs={"major_category_id": self.pk})


class User(AbstractUser):
    """
     User model
    """


    class GenderOfUser(models.TextChoices):
        """
        for detact the gender of User 
        """
        MALE = "M", 'مذکر'
        FELMALE = "F", "مونث" 

    class TypeOfUser(models.TextChoices):
        """
        for detact the gender of passengers 
        """
        REGULAR = "R", 'دانش اموز'
        SANATORUM = "S", "مصحح" 
        ADMIN = "A", "ادمین" 


    PhoneNumber = PhoneNumberField(unique=True, db_index=True, verbose_name="شماره")
    gender = models.CharField(max_length=255, choices=GenderOfUser, verbose_name="جنسیت")
    national_id = models.CharField(max_length=255, verbose_name='کد ملی', null=True) 
    
    province =  models.CharField(max_length=255, verbose_name='نام استان', null=True) 
    city =  models.CharField(max_length=255, verbose_name='نام شهر', null=True) 
    school =  models.CharField(max_length=255, verbose_name='نام مدرسه', null=True) 
    
    grade =  models.ForeignKey(GradeCategories, related_name='users', null=True, on_delete=models.PROTECT, verbose_name='پایه') 
    major =  models.ForeignKey(MajorCategories, related_name='users', null=True, on_delete=models.PROTECT, verbose_name='رشته تحصیلی') 
    
    father_name =  models.CharField(max_length=255, verbose_name='نام پدر', null=True) 
    private_code =  models.CharField(max_length=1000, verbose_name='کد مخفی کاربر', null=True, blank=True) 
    birth = models.DateTimeField(verbose_name='تاریخ تولد', null=True)

    otp = models.CharField(max_length=6, blank=True, null=True, verbose_name="کد otp")
    login_temp = models.PositiveSmallIntegerField(default=0, verbose_name="دفعات ورود")
    otp_expiry_date = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انقضای ")
    type_of_user = models.CharField(max_length=255, choices=TypeOfUser, verbose_name='نوع کاربر', default=TypeOfUser.REGULAR)

    is_verified = models.BooleanField(default=True, verbose_name='تایید شماره همراه')
    
    USERNAME_FIELD = "PhoneNumber"
    username = None

    objects = UserManager()


    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f"{str(self.PhoneNumber).replace(' ', '')}"
    
    def set_otp(self) -> int:
 
        self.otp_expiry_date = now() + timedelta(seconds=int(OTP_EXPIRATIONS_SECONDS))
        self.otp = randint(100000, 999999)
  
        if self.login_temp > LOGIN_TEMP:
            self.is_verified=False
            self.is_active=False
            self.save()

        else:
            self.login_temp+=1
            self.save()

        return self.otp

    def verify_otp(self, otp: str) -> list:

        if (int(self.otp) == int(otp)) and (self.otp_expiry_date >= now()):
            self.otp = ""
            self.otp_expiry_date = None
            self.is_verified = True
            self.login_temp = 0
            self.private_code = None
            self.save()
 
            return [200, 'verified']
        elif (int(self.otp) != int(otp)) and (self.otp_expiry_date >= now()): return [401, 'کد اعتبار سنجی اشتباه است']
        elif (int(self.otp) == int(otp)) and (self.otp_expiry_date < now()): return [402, 'زمان وارد کردن کد تمام شده است لطفا دوباره امتحان فرمایید']