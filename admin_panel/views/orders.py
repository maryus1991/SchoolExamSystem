from order.models import  Order, OrderDetail, Discount
from django.views.generic import ListView, CreateView, UpdateView, RedirectView
from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import reverse, reverse_lazy
from admin_panel.mixins import AdminPermissionRequire
from django.utils.timezone import now
from django.contrib import messages

class OrdersListView(AdminPermissionRequire, ListView):
    """for list the orders"""

    context_object_name = 'items'
    queryset = Order.objects.prefetch_related('user').all()
    template_name = 'admin-panel/orders/list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs) 

        data['status'] = Order.OrderStatus

        return data

class OrderDetailsListVies(AdminPermissionRequire, ListView):
    """for list the order details"""

    context_object_name = 'items'
    queryset = OrderDetail.objects.prefetch_related('order', 'order__user', 'quiz').all()
    template_name = 'admin-panel/orders/detail.html'
    paginate_by = 50

    def get_queryset(self):
        self.order = Order.objects.prefetch_related('user', 'details', 'details__quiz', 'details__quiz__grade', 'details__quiz__lession', 'details__quiz__major')
        self.order =  get_object_or_404(self.order, pk=self.kwargs.get('pk'))
        return self.order.details.all()
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['order'] = self.order

        return data 
    
    

class OrderCancellByAdmin(AdminPermissionRequire, RedirectView):
    """for cancell the order by admin """

    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(Order, pk=kwargs.get('pk'))


        if item.status == Order.OrderStatus.active:
            item.status = Order.OrderStatus.cancelled_by_admin
            item.update_at = now()
            item.save()
            messages.warning(
                self.request, 'سفارش مورد نظر کنسل شد'
            )
 

        return reverse('admin-panel:order-list')
    
class OrderSubmitByAdmin(AdminPermissionRequire, RedirectView):
    """for cancell the order by admin """

    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(Order, pk=kwargs.get('pk'))

 
        item.status = Order.OrderStatus.paid
        item.update_at = now()
        item.save()
        
        messages.warning(
            self.request, 'سفارش مورد نظر تایید شد'
        )

        for detail in item.details.all():
            detail.quiz.student.add(
                item.user
            )
            detail.quiz.detail.get_or_create(
                student=item.user
            )
 

        return reverse('admin-panel:order-detail', kwargs={'pk': item.id})