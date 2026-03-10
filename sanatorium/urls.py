from django.urls import path

from . import views

app_name = 'sanatorium'

urlpatterns = [
    path('', views.profile.SanatoriumPanel.as_view(), name='main'),
    path('1', views.profile.SanatoriumPanel1.as_view(), name='main1'),
    path('2', views.profile.SanatoriumPanel2.as_view(), name='main2'),
    path('3', views.profile.SanatoriumPanel3.as_view(), name='main3'),
    path('4', views.profile.SanatoriumPanel4.as_view(), name='main4'),
    path('5', views.profile.SanatoriumPanel5.as_view(), name='main5'),
    path('6', views.profile.SanatoriumPanel6.as_view(), name='main6'),
    path('7', views.profile.SanatoriumPanel7.as_view(), name='main7'),
    path('8', views.profile.SanatoriumPanel8.as_view(), name='main8'),
    path('9', views.profile.SanatoriumPanel9.as_view(), name='main9'),
    path('10', views.profile.SanatoriumPanel10.as_view(), name='main10'),
]
