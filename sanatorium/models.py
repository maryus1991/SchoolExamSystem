from django.db import models
from user.models import User
from quiz.models import Quiz, StudentAnswer
from django.urls import reverse

# Create your models here.

class SanatoriumWallet(models.Model):
    user = models.ForeignKey(User,related_name='wallet', verbose_name='کاربر', on_delete=models.PROTECT)
    quiz = models.ForeignKey(Quiz, related_name='wallet', on_delete=models.PROTECT, verbose_name='ازمون')

    final_price = models.PositiveBigIntegerField(verbose_name='قیمت', default=0)
 
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن')
    
    class OrderStatus(models.TextChoices):
        active = 'جاری', 'جاری'
        paid = 'تصفیه شده', 'تصفیه شده'

    status = models.CharField(verbose_name='وضعیت', choices=OrderStatus, default=OrderStatus.active)

    def __str__(self):
        return f'{self.id} - {self.user.id} - {self.status}'
    
    class Meta:
        ordering = ['-pk']
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف پول ها'

    def get_absolute_url(self):
        return reverse("sanatorium:wallet-detail", kwargs={"pk": self.id})

    def get_payment_price(cls):
        
        if cls.status == cls.OrderStatus.active or cls.final_price <= 0:
            price = 0 
            for item in cls.details.filter(is_active=True).all():
                price += item.get_item_price()
                
            cls.final_price = price
            cls.save()
            return price
        else:
            return cls.final_price 
            

class WalletDetails(models.Model):
    wallet = models.ForeignKey(SanatoriumWallet, related_name='details', on_delete=models.PROTECT, verbose_name='کیف پول')
    answer = models.ForeignKey(StudentAnswer, related_name='wallet', on_delete=models.PROTECT, verbose_name='پاسخ نامه')

    price = models.PositiveBigIntegerField(verbose_name='قیمت', default=0)
    create_at = models.DateTimeField(auto_now_add=True,  verbose_name='تاریخ افزودن')
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن')


    def __str__(self):
        return f'{self.wallet.quiz.name} - {self.id} - {self.wallet.user.id} - {self.wallet.status}'
    
    class Meta:
        ordering = ['-pk']
        verbose_name = 'جزییات کیف پول'
        verbose_name_plural = 'جزییات کیف پول'


    def get_item_price(cls):
        if cls.wallet.status == SanatoriumWallet.OrderStatus.active or cls.price <= 0:
            cls.price = cls.wallet.quiz.corrected_price
            cls.save()
            return cls.wallet.quiz.corrected_price
        else:
            return cls.price