from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from user.models import User
from easy_thumbnails.fields import ThumbnailerImageField
from django.utils.crypto import get_random_string
from django.urls import reverse

def photo_path_upload_to(*args, **kwargs):
    return f"blog/images/{get_random_string(72)}"


class Blog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        related_name="blogs",
        verbose_name="نویسنده",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="زمان انتشار")

    title = models.CharField(max_length=100, verbose_name="عنوان")
    category = models.CharField(max_length=255, verbose_name="دسته")
    short_content = models.CharField(max_length=100, verbose_name="توضیحات کوتاه")
    content = CKEditor5Field(verbose_name="متن یا بدنه")
    time_to_read_minutes = models.PositiveSmallIntegerField(default=10, verbose_name='زمان مطاعه بع دقیقه') 
    image = ThumbnailerImageField(verbose_name='عکس', upload_to=photo_path_upload_to)
    is_active = models.BooleanField(
        default=False, verbose_name="فعال / غیر فعال "
    )

    sort_number = models.PositiveBigIntegerField(default=0, verbose_name='ترتیب نمایش')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-sort_number']

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})


class BlogView(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="views")
    ip = models.GenericIPAddressField()
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip