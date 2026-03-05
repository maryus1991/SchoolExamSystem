from django.db import models
from quiz.models import Quiz
from user.models import User


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.PROTECT, related_name='order')
    final_price = models.PositiveBigIntegerField(verbose_name='قیمت', null=True, blank=True)
    
    class OrderStatus(models.TextChoices):
        active = 'فعال', 'فعال'
        cancelled = 'کنسل شده', 'کنسل شده'
        paid = 'پرداخت شده', 'پرداخت شده'

    status = models.CharField(verbose_name='وضعیت', choices=OrderStatus, default=OrderStatus.active)

    def __str__(self):
        return f'{self.id} - {self.user.id} - {self.status}'
    
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='detail')
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT, related_name='order')
    price = models.PositiveBigIntegerField(verbose_name='', null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.user.id} - {self.status}'
    
    class Meta:
        verbose_name = 'جزییات سفارش'
        verbose_name_plural = 'جزییات سفارشات'