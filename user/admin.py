from django.contrib import admin

from .models import User, MajorCategories, GradeCategories

admin.site.register(User)
admin.site.register(MajorCategories)
admin.site.register(GradeCategories)