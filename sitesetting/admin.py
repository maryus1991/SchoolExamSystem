from django.contrib import admin
from .models import ContactUs, Newsletter, QuestionAndAnswer, Site, SiteLaw, Team
# Register your models here.

admin.site.register(Site)
admin.site.register(SiteLaw)
admin.site.register(Team)
admin.site.register(ContactUs)
admin.site.register(QuestionAndAnswer)
admin.site.register(Newsletter)





