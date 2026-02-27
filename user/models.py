from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import timedelta, now
from random import randint
from .managers import UserManager
from config.settings import OTP_EXPIRATIONS_MINUTES
 

# Create your models here.

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


    gender = models.CharField(max_length=255, choices=GenderOfUser, verbose_name="جنسیت")
    PhoneNumber = PhoneNumberField(unique=True, db_index=True, verbose_name="شماره")
    otp = models.CharField(max_length=6, blank=True, null=True, verbose_name="کد otp")
    otp_expiry_date = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انقضای ")
    type_of_user = models.CharField(max_length=255, choices=TypeOfUser, verbose_name='نوع کاربر', default=TypeOfUser.REGULAR)
    national_id = models.CharField(max_length=255, verbose_name='کد ملی') 
    province =  models.CharField(max_length=255, verbose_name='نام استان') 
    city =  models.CharField(max_length=255, verbose_name='نام شهر') 
    school =  models.CharField(max_length=255, verbose_name='نام مدرسه') 
    grade =  models.CharField(max_length=255, verbose_name='پایه') 
    major =  models.CharField(max_length=255, verbose_name='رشته تحصیلی') 
    father_name =  models.CharField(max_length=255, verbose_name='نام پدر') 
    birth = models.DateTimeField(verbose_name='تاریخ تولد') 

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
 
        self.otp_expiry_date = now() + timedelta(minutes=int(OTP_EXPIRATIONS_MINUTES))
        self.otp = randint(100000, 999999)

        self.save()

        return self.otp

    def verify_otp(self, otp: str) -> list:

        if (int(self.otp) == int(otp)) and (self.otp_expiry_date >= now()):
            self.otp = ""
            self.otp_expiry_date = None

            self.save()
 
            return [200, 'verified']
        elif (int(self.otp) != int(otp)) and (self.otp_expiry_date >= now()): return [401, 'otp code is wrong']
        elif (int(self.otp) == int(otp)) and (self.otp_expiry_date < now()): return [402, 'otp code has been expired']