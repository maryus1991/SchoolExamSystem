from django.db import models
from quiz.models import Quiz
from user.models import User


class Order(models.Model):
    user = models.ForeignKey(User,related_name='orders', verbose_name='کاربر', on_delete=models.PROTECT)
    final_price = models.PositiveBigIntegerField(verbose_name='قیمت', null=True, blank=True)

    authority = models.CharField(max_length=120, null=True, blank=True, unique=True, verbose_name='کد درگاه پرداخت')
    cart = models.CharField(max_length=120, null=True, blank=True, verbose_name='کارت')
    cart_hash = models.CharField(max_length=120, null=True, blank=True, verbose_name='کارت هش شده')
    payment_id = models.PositiveBigIntegerField(default=0, verbose_name='کد پیگیری')
    ZarinPal_fee = models.PositiveBigIntegerField(default=0, verbose_name='هزینه اخذ شده توسط درگاه پرداخت')

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن')

    
    class OrderStatus(models.TextChoices):
        active = 'جاری', 'جاری'
        cancelled = 'کنسل شده', 'کنسل شده'
        cancelled_by_admin = 'کنسل شده توسط ادمین', 'کنسل شده توسط ادمین'
        paid = 'پرداخت شده', 'پرداخت شده'

    status = models.CharField(verbose_name='وضعیت', choices=OrderStatus, default=OrderStatus.active)

    def __str__(self):
        return f'{self.id} - {self.user.id} - {self.status}'
    
    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='details', on_delete=models.PROTECT, verbose_name='سبد خرید')
    quiz = models.ForeignKey(Quiz, related_name='orders', on_delete=models.PROTECT, verbose_name='ازمون')
    price = models.PositiveBigIntegerField(verbose_name='قیمت', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True,  verbose_name='تاریخ ساخت')
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن')


    def __str__(self):
        return f'{self.id} - {self.user.id} - {self.status}'
    
    class Meta:
        verbose_name = 'جزییات سفارش'
        verbose_name_plural = 'جزییات سفارشات'


class Discount(models.Model):
    user = models.ManyToManyField(User,related_name='discounts', verbose_name='کاربر',   )
    order = models.ManyToManyField(Order, related_name='discounts',  verbose_name='سبد های خرید',)
    quiz = models.ManyToManyField(Quiz, related_name='discounts',  verbose_name='ازمون ها',)
    price = models.PositiveBigIntegerField(verbose_name='مبلغ تخفیف (اختیاری)', null=True, blank=True)
    percent = models.PositiveBigIntegerField(verbose_name='درصد تخفیف (اختیاری)', null=True, blank=True)
    min_price = models.PositiveBigIntegerField(default=0, verbose_name='حداقل قیمت جهت اعمال تخفیف')
    end_date_discount = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ پایان')
    start_date_discount = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ شروع')
    count = models.PositiveBigIntegerField(default=0, verbose_name='تعداد')
    name = models.CharField(max_length=100, null=True, blank=True, unique=True, db_index=True, verbose_name='نام')
    count_of_use_per_user = models.PositiveIntegerField(default=1, verbose_name='اجازه استفاده برای هر کاربر')
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن')

    def __str__(self):
        return f"{self.name} - {self.id}"
    
    class Meta:
        verbose_name = 'کد تخفیف '
        verbose_name_plural = 'کد تخفیف ها'