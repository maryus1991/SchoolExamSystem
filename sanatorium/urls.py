from django.urls import path

from . import views

app_name = 'sanatorium'

urlpatterns = [
    path('', views.profile.SanatoriumPanel.as_view(), name='main')
]
