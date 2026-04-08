from sanatorium.models import SanatoriumWallet, WalletDetails
from django.views.generic import ListView, RedirectView
from admin_panel.mixins import AdminPermissionRequire
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db.models.aggregates import Count

class WalletsListView(AdminPermissionRequire, ListView):
    """ for list the wallets """
    context_object_name='items'
    template_name = 'admin-panel/wallets/list.html'
    paginate_by = 50

    
    queryset = SanatoriumWallet.objects.prefetch_related('quiz', 'user', 'details').annotate(detail_count=Count('details')).all()

    
    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        data['status'] = SanatoriumWallet.OrderStatus
        return data


class WalletDetailListView(AdminPermissionRequire, ListView):
    """ for list the wallet detail """  

    context_object_name='items'
    template_name = 'admin-panel/wallets/detail.html'
    paginate_by = 50

    def get_queryset(self):
        self.pk = self.kwargs.get('pk')
        self.wallet = get_object_or_404(SanatoriumWallet.objects.prefetch_related('quiz', 'details'), id=self.pk)
        return self.wallet.details.prefetch_related('answer').all()
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['wallet'] =  self.wallet
        data['status'] =  SanatoriumWallet.OrderStatus

        return data

class WalletChangeStatus(AdminPermissionRequire, RedirectView):
    """ for paid the request payment """

    def get_redirect_url(self, *args, **kwargs):

        wallet = get_object_or_404(SanatoriumWallet, pk=kwargs.get('pk'))
        wallet.get_payment_price()
        wallet.status = SanatoriumWallet.OrderStatus.paid
        wallet.save()
        messages.success(self.request, 'کیف پول به وضعیت پرداخت شده تبدیل شد')

        return reverse('admin-panel:wallet-detail', kwargs=kwargs)
