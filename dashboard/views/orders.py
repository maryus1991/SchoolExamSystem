from django.views.generic import ListView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import User
from quiz.models import Quiz
from order.models import Order, OrderDetail
from django.shortcuts import get_object_or_404


class OrdersList(LoginRequiredMixin, ListView):
    """for listing the orders"""
    
    template_name = 'dashboard/order/orders.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True).all()
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)    

        data['status'] = Order.OrderStatus
        return data
    

class OrderDetailsList(LoginRequiredMixin, ListView):
    """for listing the details of the order"""
    template_name = 'dashboard/order/detail.html'
    context_object_name = 'items'

    def get_queryset(self):
        self.order = get_object_or_404(Order, pk=self.kwargs.get('pk'), user=self.request.user)
        return OrderDetail.objects.filter(is_active=True, order=self.order).prefetch_related('order', 'quiz').all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)    

        data['order'] = self.order
        return data