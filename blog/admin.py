from django.contrib import admin
from .models import Blog, BlogView
# Register your models here.

admin.site.register(Blog)
admin.site.register(BlogView)