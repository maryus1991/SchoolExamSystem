from django.urls import path
from . import views

app_name = 'admin-panel'

urlpatterns = [

    path('', views.site.Main.as_view(), name='main'),
    
    # users
    path('users/', views.users.UserListView.as_view(), name='user-list'),
    path('users/create/', views.users.UserCreate.as_view(), name='user-create'),
    path('users/update/<int:pk>', views.users.UserUpdate.as_view(), name='user-update'),
    path('users/active/<int:pk>', views.users.UserActiveDeactivate.as_view(), name='user-active'),
    path('users/verify/<int:pk>', views.users.UserVerifyUnverify.as_view(), name='user-verify'),

    # categories
    # major
    path('categories/major/', views.categories.MajorListView.as_view(), name='categories-major-list'),
    path('categories/major/create/', views.categories.MajorCreate.as_view(), name='categories-major-create'),
    path('categories/major/update/<int:pk>', views.categories.MajorUpdate.as_view(), name='categories-major-update'),
    path('categories/major/active/<int:pk>', views.categories.MajorActiveDeactivate.as_view(), name='categories-major-active'),
    # lession
    path('categories/lession/', views.categories.LessionListView.as_view(), name='categories-lession-list'),
    path('categories/lession/create/', views.categories.LessionCreate.as_view(), name='categories-lession-create'),
    path('categories/lession/update/<int:pk>', views.categories.LessionUpdate.as_view(), name='categories-lession-update'),
    path('categories/lession/active/<int:pk>', views.categories.LessionActiveDeactivate.as_view(), name='categories-lession-active'),
    # grade
    path('categories/grade/', views.categories.GradeListView.as_view(), name='categories-grade-list'),
    path('categories/grade/create/', views.categories.GradeCreate.as_view(), name='categories-grade-create'),
    path('categories/grade/update/<int:pk>', views.categories.GradeUpdate.as_view(), name='categories-grade-update'),
    path('categories/grade/active/<int:pk>', views.categories.GradeActiveDeactivate.as_view(), name='categories-grade-active'),
    # possible
    path('categories/possible/', views.categories.PossibleListView.as_view(), name='categories-possible-list'),
    path('categories/possible/create/', views.categories.PossibleCreate.as_view(), name='categories-possible-create'),
    path('categories/possible/update/<int:pk>', views.categories.PossibleUpdate.as_view(), name='categories-possible-update'),
    path('categories/possible/active/<int:pk>', views.categories.PossibleActiveDeactivate.as_view(), name='categories-possible-active'),
    # TicketProblemPlacement
    path('categories/ticket/placemnt/', views.categories.TicketProblemPlacementListView.as_view(), name='categories-TicketProblemPlacement-list'),
    path('categories/ticket/placemnt/create/', views.categories.TicketProblemPlacementCreate.as_view(), name='categories-TicketProblemPlacement-create'),
    path('categories/ticket/placemnt/update/<int:pk>', views.categories.TicketProblemPlacementUpdate.as_view(), name='categories-TicketProblemPlacement-update'),
    path('categories/ticket/placemnt/active/<int:pk>', views.categories.TicketProblemPlacementActiveDeactivate.as_view(), name='categories-TicketProblemPlacement-active'),
    # TicketProblemCategory
    path('categories/ticket/problem/', views.categories.TicketProblemCategoryListView.as_view(), name='categories-TicketProblemCategory-list'),
    path('categories/ticket/problem/create/', views.categories.TicketProblemCategoryCreate.as_view(), name='categories-TicketProblemCategory-create'),
    path('categories/ticket/problem/update/<int:pk>', views.categories.TicketProblemCategoryUpdate.as_view(), name='categories-TicketProblemCategory-update'),
    path('categories/ticket/problem/active/<int:pk>', views.categories.TicketProblemCategoryActiveDeactivate.as_view(), name='categories-TicketProblemCategory-active'),


    # blog
    path('blog/', views.blog.BlogList.as_view(), name='blog-list'),
    path('blog/create/', views.blog.BlogCreate.as_view(), name='blog-create'),
    path('blog/update/<int:pk>', views.blog.BlogUpdate.as_view(), name='blog-update'),
    path('blog/active/<int:pk>', views.blog.BlogActiveDeactivate.as_view(), name='blog-active'),
    path('blog/delete/<int:pk>', views.blog.BlogDelete.as_view(), name='blog-delete'),

    # orders
    path('orders', views.orders.OrdersListView.as_view(), name='order-list'),
    path('orders/<int:pk>', views.orders.OrderDetailsListVies.as_view(), name='order-detail'),
    path('orders/submitting/<int:pk>', views.orders.OrderSubmitByAdmin.as_view(), name='order-admin-submmiting'),
    path('orders/cancell-by-admin/<int:pk>', views.orders.OrderCancellByAdmin.as_view(), name='order-cancel-by-admin'),

    # tickets
    path('tickets/', views.tickets.TicketListViews.as_view(), name='ticket-list'),
    path('tickets/<int:pk>', views.tickets.TicketChat.as_view(), name='ticket-chat'),

    # question bank
    path('question-bank/', views.qbank.QuestionBankListView.as_view(), name='qbank-list'),
    path('question-bank/active-deactivate/<int:pk>', views.qbank.QbankActiveDeactivate.as_view(), name='qbank-active'),
    path('question-bank/delete/<int:pk>', views.qbank.QbankDelete.as_view(), name='qbank-delete'),
    
    path('question-bank/create/', views.qbank.QbankCreateView.as_view(), name='qbank-create'),
    path('question-bank/create/option/<int:pk>', views.qbank.QbankOptionCreate.as_view(), name='qbank-create-option'),
    path('question-bank/create/key/<int:pk>', views.qbank.QbankAnswerKey.as_view(), name='qbank-create-key'),

    path('question-bank/update/<int:pk>', views.qbank.QbankUpdateView.as_view(), name='qbank-update'),
    path('question-bank/update/option/<int:pk>', views.qbank.QbankOptionUpdateView.as_view(), name='qbank-option-update'),
    path('question-bank/update/key/<int:pk>', views.qbank.QbankAnswerKeyUpdateView.as_view(), name='qbank-key-update'),

    path('question-bank/delete/option/<int:pk>', views.qbank.QuestionOptionDelete.as_view(), name='qbank-option-delete'),

    path('question-bank/key/delete/<int:pk>/image', views.qbank.QuestionKeyDeleteImage.as_view(), name='qbank-questionskey-delete-image'),
    path('question-bank/key/delete/<int:pk>/pdf', views.qbank.QuestionKeyDeletePDF.as_view(), name='qbank-questionskey-delete-pdf'),
    path('question-bank/delete/<int:pk>/image', views.qbank.QuestionDeleteImage.as_view(), name='qbank-questions-delete-image'),
    path('question-bank/delete/<int:pk>/pdf', views.qbank.QuestionDeletePDF.as_view(), name='qbank-questions-delete-pdf'),

    # site 
    path('site/update', views.site.SiteUpdateView.as_view(), name='site'),

    # site law
    path('site/law/', views.site.SiteLawListView.as_view(), name='site-law-list'),
    path('site/law/create/', views.site.SiteLawCreateView.as_view(), name='site-law-create'),
    path('site/law/update/<int:pk>', views.site.SiteLawUpdateView.as_view(), name='site-law-update'),

    # site Q&A 
    path('site/Q&A/', views.site.QuestionAndAnswerListView.as_view(), name='site-qa-list'),
    path('site/Q&A/create/', views.site.QuestionAndAnswerCreateView.as_view(), name='site-qa-create'),
    path('site/Q&A/update/<int:pk>', views.site.QuestionAndAnswerUpdateView.as_view(), name='site-qa-update'),

    # site team
    path('site/team/', views.site.TeamListView.as_view(), name='site-team-list'),
    path('site/team/create/', views.site.TeamCreateView.as_view(), name='site-team-create'),
    path('site/team/update/<int:pk>', views.site.TeamUpdateView.as_view(), name='site-team-update'),

    # wallet 
    path('wallets/', views.wallet.WalletsListView.as_view(), name='wallet-list'),
    path('wallets/<int:pk>/details', views.wallet.WalletDetailListView.as_view(), name='wallet-detail'),
    path('wallets/<int:pk>/paid', views.wallet.WalletChangeStatus.as_view(), name='wallet-paid'),
    
    # quiz
    path('exam/', views.quiz.QuizListView.as_view(), name='quiz-list'),
    path('exam/create/', views.quiz.QuizCreateView.as_view(), name='quiz-create'),
    path('exam/update/<int:pk>', views.quiz.QuizUpdateView.as_view(), name='quiz-update'),
    path('exam/active/<int:pk>', views.quiz.QuizActivateView.as_view(), name='quiz-active'),
    path('exam/start-currecting/<int:pk>', views.quiz.QuizStartCurrectingView.as_view(), name='quiz-currecting'),

    # questions
    path('exam/<int:quiz_id>/questions/', views.quiz.QuestionListView.as_view(), name='quiz-questions-list'),
    path('exam/<int:quiz_id>/questions/create/', views.quiz.QuestionCreateView.as_view(), name='quiz-questions-create'),
    path('exam/<int:quiz_id>/questions/update/<int:pk>', views.quiz.QuestionUpdateView.as_view(), name='quiz-questions-update'),
    path('exam/<int:quiz_id>/questions/delete/<int:pk>', views.quiz.QuestionDelete.as_view(), name='quiz-questions-delete'),
    path('exam/<int:quiz_id>/questions/delete/<int:pk>/image', views.quiz.QuestionDeleteImage.as_view(), name='quiz-questions-delete-image'),
    path('exam/<int:quiz_id>/questions/delete/<int:pk>/pdf', views.quiz.QuestionDeletePDF.as_view(), name='quiz-questions-delete-pdf'),

    # question key
    path('exam/<int:quiz_id>/question/<int:qid>/key/create/', views.quiz.QuestionAnswerKeyCreateView.as_view(), name='quiz-question-key-create'),
    path('exam/<int:quiz_id>/question/<int:qid>/key/update/', views.quiz.QuestionAnswerKeyUpdateView.as_view(), name='quiz-question-key-update'),
    path('exam/<int:quiz_id>/question/<int:qid>/key/delete/<int:pk>/image', views.quiz.QuestionKeyDeleteImage.as_view(), name='quiz-questions-key-delete-image'),
    path('exam/<int:quiz_id>/question/<int:qid>/key/delete/<int:pk>/pdf', views.quiz.QuestionKeyDeletePDF.as_view(), name='quiz-questions-key-delete-pdf'),

    # question option
    path('exam/<int:quiz_id>/question/<int:qid>/options/create/', views.quiz.QuestionOptionsCreateView.as_view(), name='quiz-question-option-create'),
    path('exam/<int:quiz_id>/question/<int:qid>/options/update/<int:pk>', views.quiz.QuestionOptionsUpdateView.as_view(), name='quiz-question-option-update'),
    path('exam/<int:quiz_id>/question/<int:qid>/options/delete/<int:pk>', views.quiz.QuestionOptionDelete.as_view(), name='quiz-question-option-delete'),

    # quiz questions answer 
    path('exam/<quiz_id>/question/<int:qid>/answers/', views.quiz.QuestionAnswerLitView.as_view(), name='quiz-question-answer-list'),
    path('exam/<quiz_id>/question/<int:qid>/answer/<int:pk>', views.quiz.QuestionAnswerUpdateView.as_view(), name='quiz-question-answer-update'),
 
    
    # reports 
    path('reports/', views.reports.ReportListView.as_view(), name='report-list'),
    path('reports/<int:quiz_id>', views.reports.ReportListView.as_view(), name='report-quiz-list'),
    path('reports/create', views.reports.ReportCreateView.as_view(), name='report-create'),
    path('reports/update/<int:pk>', views.reports.ReportUpdateView.as_view(), name='report-update'),
    
]

