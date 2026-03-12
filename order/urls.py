from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('add-to-order/<int:pk>', views.AddToOrder.as_view(), name='add'),
    path('start-payment/<int:pk>', views.StartPayment.as_view(), name='start-payment'),
    path('verfiy-payment/<int:pk>', views.VerifyPayment.as_view(), name='verfiy-payment')
]
