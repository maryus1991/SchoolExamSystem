from django.urls import path
from . import views

app_name='dashboard'


urlpatterns = [

    # main

    path('', views.profile.Dashboard.as_view(), name='main'), 
    path('profile/', views.profile.Profile.as_view(), name='profile'), 

    # qbank

    path('qbank/', views.qbank.QuestionList.as_view(), name='qbank-list'), 
    path('qbank/<int:pk>', views.qbank.QuestionDetail.as_view(), name='qbank-detail'), 

    # quiz

    path('quiz/', views.quiz.QuizList.as_view(), name='quiz-list'), 
    path('quiz/<int:pk>', views.quiz.QuizDetail.as_view(), name='quiz-detail'), 

    # ticket

    path('ticket/', views.tickets.Ticketlist.as_view(), name='ticket-list'), 
    path('ticket/<int:pk>', views.tickets.TicketChat.as_view(), name='ticket-chat'), 
    path('ticket/send/', views.tickets.TicketSend.as_view(), name='ticket-send'), 

    # ticket

    path('report/third/', views.report.ThirdReport.as_view(), name='report-third'), 
    path('report/second/', views.report.SecontReportList.as_view(), name='report-second-list'), 
    path('report/second/<int:pk>', views.report.SecondRespotDetail.as_view(), name='report-second-detail'), 
    path('report/first/', views.report.FirstReportList.as_view(), name='report-first-list'), 
    path('report/first/<int:pk>', views.report.FirstReportDetail.as_view(), name='report-fist-detail'), 
 
]
