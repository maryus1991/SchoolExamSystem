from django.views.generic import ListView, RedirectView
from sanatorium.models import WalletDetails, SanatoriumWallet
from django.http import Http404
from sanatorium.mixins import SanatorPermissionRequire
from django.db.models.aggregates import Count
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

class WalletListView(SanatorPermissionRequire, ListView):
    """ for list the wallets """
    context_object_name='items'
    template_name = 'sanatorium/orders/list.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = SanatoriumWallet.objects.filter(
            user=self.request.user
        ).prefetch_related('quiz', 'details'
        ).annotate(detail_count=Count('details')
        ).all()

        return queryset
    
    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        data['status'] = SanatoriumWallet.OrderStatus
        return data

class WalletDetailListView(SanatorPermissionRequire, ListView):
    """ for list the wallet detail """

    context_object_name='items'
    template_name = 'sanatorium/orders/detail.html'
    paginate_by = 50

    def get_queryset(self):
        self.pk = self.kwargs.get('pk')
        self.wallet = get_object_or_404(SanatoriumWallet, user=self.request.user, id=self.pk)
        return self.wallet.details.all()
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['wallet'] =  self.wallet
        data['status'] =  SanatoriumWallet.OrderStatus

        return data
    
class WalletRequestPayment(SanatorPermissionRequire, RedirectView):
    """ for request payment """

    def get_redirect_url(self, *args, **kwargs):

        wallet = get_object_or_404(SanatoriumWallet, pk=kwargs.get('pk'), user=self.request.user)
        wallet.get_payment_price()
        wallet.status = SanatoriumWallet.OrderStatus.request_to_paid
        wallet.update_at = now() 
        wallet.save()
        messages.success(self.request, 'درخواست شما به ادمین ارسال شد')

        return reverse('admin-panel:wallet-list', kwargs=kwargs)
