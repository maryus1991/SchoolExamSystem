from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('add-to-order/<int:pk>', views.AddToOrder.as_view(), name='add')
]
