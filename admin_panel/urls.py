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


    # blog
    path('blog/', views.blog.BlogList.as_view(), name='blog-list'),
    path('blog/create/', views.blog.BlogCreate.as_view(), name='blog-create'),
    path('blog/update/<int:pk>', views.blog.BlogUpdate.as_view(), name='blog-update'),
    path('blog/active/<int:pk>', views.blog.BlogActiveDeactivate.as_view(), name='blog-active'),
    path('blog/delete/<int:pk>', views.blog.BlogDelete.as_view(), name='blog-delete'),

]

