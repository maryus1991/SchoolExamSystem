from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_ckeditor_5.fields import CKEditor5Field 
# Create your models here.


class Newsletter(models.Model):
    phone_number = PhoneNumberField()

    def __str__(self):
        return str(self.phone_number).replace(' ','')


class QuestionAndAnswer(models.Model):
    question = models.TextField(verbose_name="سوال")
    answer = models.TextField(verbose_name="جواب")

    is_active = models.BooleanField(default=True, verbose_name="فعال یا غیر فعال")

    def __str__(self):
        return self.question


class ContactUs(models.Model):
    subject = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField()
    message = models.TextField()
    admin_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.email} - {self.phone}"


class SiteLaw(models.Model):
    name = models.CharField(verbose_name="نام قانون", max_length=250)
    description = CKEditor5Field (
         verbose_name="توضیحات "
    )
    is_active = models.BooleanField(
        default=True,
    )
    sort_number = models.IntegerField(default=0)
