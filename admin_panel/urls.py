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
]
