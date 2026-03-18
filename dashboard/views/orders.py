from django.views.generic import ListView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import User
from quiz.models import Quiz
from order.models import Order, OrderDetail
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from django.contrib import messages

class OrdersList(LoginRequiredMixin, ListView):
    """for listing the orders"""
    
    template_name = 'dashboard/order/orders.html'
    context_object_name = 'items'
    paginate_by = 50


    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True).annotate(details_count=Count("details")).all()
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)    

        data['status'] = Order.OrderStatus
        return data
    

class OrderDetailsList(LoginRequiredMixin, ListView):
    """for listing the details of the order"""
    template_name = 'dashboard/order/detail.html'
    context_object_name = 'items'
    paginate_by = 50


    def get_queryset(self):
        self.order = get_object_or_404(Order, pk=self.kwargs.get('pk'), user=self.request.user)
        return OrderDetail.objects.filter(is_active=True, order=self.order
                ).prefetch_related('order', 'quiz', 'quiz__lession' 
                ).annotate(question_count=Count('quiz__questions')).all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)    

        data['order'] = self.order
        data['order_status'] = Order.OrderStatus
        return data
    
class CancelOrder(LoginRequiredMixin, RedirectView):
    """for cancell order"""

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.get('pk')
        order = get_object_or_404(Order, user=self.request.user, pk=pk)
        if order.status == Order.OrderStatus.active :
            order.status = Order.OrderStatus.cancelled
            order.save()
            messages.info(self.request, 'سفارش کنسل شد')
        else:
            messages.error(self.request, 'شما اجازه کنسل کردن این سفارش را ندارید')

        return order.get_absolute_url()
    

class DeleteDetailOfOrder(LoginRequiredMixin, RedirectView):
    """for delete the detail of order"""
    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.get('pk')
        order = get_object_or_404(Order, user=self.request.user, pk=pk)
        if order.status == Order.OrderStatus.active :
            detail = get_object_or_404(OrderDetail,order=order, pk=kwargs.get('detail_id'), order__user=self.request.user)
            detail.delete()
            messages.info(self.request, 'سفارش حذف شد')
        else:
            messages.error(self.request, 'شما اجازه حذف این سفارش را ندارید')

        return order.get_absolute_url()
    