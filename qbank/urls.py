from django.urls import path
from . import views

app_name = 'qbank'

urlpatterns = [
    path('', views.QuestionsView.as_view(), name='list'),
    path('<int:pk>', views.QuestionsView.as_view(), name='detail'),
    path('categories/<int:category_id>', views.QuestionsView.as_view(), name='list-by-category'),
]
