from django.urls import path
from . import views

app_name='dashboard'


urlpatterns = [

    # main

    path('', views.profile.Dashboard.as_view(), name='main'), 
    path('profile/', views.profile.Profile.as_view(), name='profile'), 
    path('profile/change-password', views.profile.ChangePasswordView.as_view(), name='change-password'), 
    path('profile/change-phone-number', views.profile.ChangePhoneNumberNaitnalIDView.as_view(), name='change-phone-number'), 

    # favorate

    path('favorate/question-bank/', views.favorate.FavorateQuestionList.as_view(), name='qbank-list'), 
    path('favorate/blog/', views.favorate.FavorateBlogList.as_view(), name='blog-list'), 
    path('favorate/quiz/', views.favorate.FavorateQuizList.as_view(), name='favorate-quiz-list'), 
 

    # quiz

    path('quiz/', views.quiz.QuizList.as_view(), name='quiz-list'), 
    path('quiz/<int:pk>', views.quiz.QuizDetail.as_view(), name='quiz-detail'), 


    # order

    path('order/', views.orders.OrdersList.as_view(), name='order-list'), 
    path('order/<int:pk>/details/', views.orders.OrderDetailsList.as_view(), name='order-detail'), 
    path('order/<int:pk>/cancel/', views.orders.CancelOrder.as_view(), name='order-cancel'), 
    path('order/<int:pk>/delete/<int:detail_id>', views.orders.DeleteDetailOfOrder.as_view(), name='order-detail-delete'), 

    # ticket

    path('ticket/', views.tickets.Ticketlist.as_view(), name='ticket-list'), 
    path('ticket/<int:pk>', views.tickets.TicketChat.as_view(), name='ticket-chat'), 
    path('ticket/<int:pk>/cancel/', views.tickets.TicketCancelled.as_view(), name='ticket-chat-cancel'), 
    path('ticket/<int:pk>/fixed/', views.tickets.TicketFixed.as_view(), name='ticket-chat-fixed'), 
    path('ticket/send/', views.tickets.TicketSend.as_view(), name='ticket-send'), 

    # report

    path('report/third/', views.report.ThirdReport.as_view(), name='report-third'), 
    path('report/second/', views.report.SecontReportList.as_view(), name='report-second-list'), 
    # path('report/second/<int:pk>', views.report.SecondRespotDetail.as_view(), name='report-second-detail'), 
    # path('report/first/', views.report.FirstReportList.as_view(), name='report-first-list'), 
    # path('report/first/<int:pk>', views.report.FirstReportDetail.as_view(), name='report-fist-detail'), 
 
]
