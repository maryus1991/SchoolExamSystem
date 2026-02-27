from django.urls import path
from . import views

app_name = 'site'

urlpatterns = [
    path('contact/', views.Contact.as_view(), name='contact'),
    path('about/', views.About.as_view(), name='about'),
    path('', views.MainPage.as_view(), name='main'),
]
