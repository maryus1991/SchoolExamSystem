from django.urls import path
from . import views

app_name='quiz'

urlpatterns = [
    path('', views.QuizListDetailView.as_view(), name='list'),
    path('<int:pk>', views.QuizListDetailView.as_view(), name='detail'),
    path('categories/grade/<int:grade_category_id>', views.QuizListDetailView.as_view(), name='category-grade-list'),
    path('categories/lession/<int:lession_category_id>', views.QuizListDetailView.as_view(), name='category-lession-list'),
    path('categories/major/<int:major_category_id>', views.QuizListDetailView.as_view(), name='category-major-list'),
]
