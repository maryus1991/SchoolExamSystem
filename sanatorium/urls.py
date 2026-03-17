from django.urls import path

from . import views

app_name = 'sanatorium'

urlpatterns = [
    path('', views.profile.SanatoriumPanel.as_view(), name='main'),
    path('account/', views.profile.SanatoriumEditProfileInfos.as_view(), name='edit-infos'),
 
    path('exams/pending/', views.quiz_remain.SanatoriumPendingExamList.as_view(), name='exam-list'),
    path('exams/<int:pk>/students/question/detail', views.quiz_remain.SanatoriumQuestionDetailPerStudentOfExam.as_view(), name='exam-student-question-detail'),
    path('exams/<int:pk>/students/question/detail/<int:report_id>', views.quiz_remain.SanatoriumQuestionDetailPerStudentOfExam.as_view(), name='exam-student-question-detail-pk'),
    path('exams/<int:pk>/students/reports', views.quiz_remain.SanatoriumReportsListPerStudentOfExam.as_view(), name='exam-student-question-list'),

    path('wallet/', views.wallet.WalletListView.as_view(), name='wallet-list'),
    path('wallet/<int:pk>', views.wallet.WalletDetailListView.as_view(), name='wallet-detail'),
    path('wallet/<int:pk>/request-paymant', views.wallet.WalletRequestPayment.as_view(), name='wallet-payment'),

    path('ticket/', views.tickets.TicketList.as_view(), name='ticket-list'),
    path('ticket/send/', views.tickets.SendTicket.as_view(), name='ticket-send'),
    path('tikcet/<int:pk>/conversation', views.tickets.TicketConversation.as_view(), name='ticket-conversation'),
]
