from django.urls import path

from . import views

app_name = 'sanatorium'

urlpatterns = [
    path('', views.profile.SanatoriumPanel.as_view(), name='main'),
    path('account/', views.profile.SanatoriumEditProfileInfos.as_view(), name='edit-infos'),
 
    path('exams/pending/', views.quiz_remain.SanatoriumPendingExamList.as_view(), name='exam-list'),
    path('exams/<int:pk>/students/', views.quiz_remain.SanatoriumStudentListOfExam.as_view(), name='exam-student-list'),
    path('exams/pending/students/question', views.quiz_remain.SanatoriumQuestionListPerStudentOfExam.as_view(), name='exam-student-question-list'),
    path('exams/pending/students/question/detail', views.quiz_remain.SanatoriumQuestionDetailPerStudentOfExam.as_view(), name='exam-student-question-detail'),


    path('ticket/', views.tickets.TicketList.as_view(), name='ticket-list'),
    path('ticket/send/', views.tickets.SendTicket.as_view(), name='ticket-send'),
    path('tikcet/<int:pk>/conversation', views.tickets.TicketConversation.as_view(), name='ticket-conversation'),
]
