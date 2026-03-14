from django.urls import path
from . import views

app_name='quiz'

urlpatterns = [
    path('', views.QuizListDetailView.as_view(), name='list'),
    path('<int:pk>', views.QuizListDetailView.as_view(), name='detail'),
    path('<int:pk>/set-detail/', views.SetQuizDetailForUser.as_view(), name='set-details'),
    path('<int:pk>/started/', views.QuizStarted.as_view(), name='quiz-start'),
    path('<int:pk>/finished/', views.QuizFinished.as_view(), name='quiz-finished'),
    path('<int:pk>/started/<int:question_id>', views.QuizStarted.as_view(), name='quiz-start-quesion-id'),
    path('<int:pk>/skipped/<int:question_id>', views.QuizSetSkippedToQuestion.as_view(), name='quiz-skipped-quesion-id'),
    path('<int:pk>/started/<int:question_id>/set-answer/text', views.QuizSetAnswerTextOrFiles.as_view(), name='quiz-set-text-file-answer-quesion'),
    path('<int:pk>/started/<int:question_id>/set-answer/options/<int:option_id>', views.QuizSetAnswerOptions.as_view(), name='quiz-set-option-answer-quesion'),
    path('add-quiz-favorate/<int:pk>', views.AddToFavorate.as_view(), name='add-quiz-to-favorate'),
    path('remove-quiz-favorate/<int:pk>', views.RemoveToFavorate.as_view(), name='remove-quiz-to-favorate'),
    path('categories/grade/<int:grade_category_id>', views.QuizListDetailView.as_view(), name='category-grade-list'),
    path('categories/lession/<int:lession_category_id>', views.QuizListDetailView.as_view(), name='category-lession-list'),
    path('categories/major/<int:major_category_id>', views.QuizListDetailView.as_view(), name='category-major-list'),
]
