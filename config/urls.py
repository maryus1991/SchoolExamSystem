"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    # apps 
    path('blog/', include('blog.urls')), 
    path('order/', include('order.urls')),
    path('admin-panel/', include('admin_panel.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('question-bank/', include('qbank.urls')),
    path('user/', include('user.urls')),
    path('sanatorium/', include('sanatorium.urls')),
    path('quiz/', include('quiz.urls')),
    path('report/', include('report.urls')),
    path('', include('sitesetting.urls')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static.static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns = urlpatterns + static.static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )