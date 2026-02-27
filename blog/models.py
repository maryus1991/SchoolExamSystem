from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from user.models import User

# def photo_path_upload_to(*args, **kwargs):
#     return f"images/slider/{get_random_string(100)}"


class BlogCategory(models.Model):
    name = models.CharField(verbose_name="نام", max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="دسته مادر",
    )

    is_active = models.BooleanField(verbose_name="فعال / غیر فعال", default=True)
    sort_number = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Blog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        related_name="blogs",
        verbose_name="نویسنده",
    )
    title = models.CharField(max_length=100, verbose_name="عنوان")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="زمان انتشار")
    
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="blogs",
        verbose_name="دسته",
    )
    content = CKEditor5Field(verbose_name="متن یا بدنه")

    is_active = models.BooleanField(
        default=False, verbose_name="فعال / غیر فعال برای انتشار توسط فروشگاه"
    )

    sort_number = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("blog:detail", kwargs={"pk": self.pk})


class BlogView(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="views")
    ip = models.GenericIPAddressField()
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip