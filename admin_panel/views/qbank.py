from django.views.generic import CreateView, ListView, RedirectView
from django.contrib import messages 
from qbank.models import QuestionBank, QuestionOption, QuestionAnswerKey
from admin_panel.mixins import AdminPermissionRequire
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

class QuestionBankListView(AdminPermissionRequire, ListView):
    """for list the questions"""

    context_object_name = 'items'
    template_name = 'admin-panel/question-bank/list.html'
    queryset = QuestionBank.objects.prefetch_related('possible', 'category').all()
    paginate_by = 250

class QbankDelete(AdminPermissionRequire, RedirectView):
    """for deactivate or activate the question """

    model = QuestionBank
    success_url = reverse_lazy('admin-panel:qbank-list')

    def get_redirect_url(self, *args, **kwargs):

        pk = kwargs.get('pk')

        item = get_object_or_404(self.model, pk=pk)
        item.delete()

        messages.warning(self.request, 'سوال مورد نظر حذف شد')

        return self.success_url

class QbankActiveDeactivate(AdminPermissionRequire, RedirectView):
    """for deactivate or activate the question """

    model = QuestionBank
    success_url = reverse_lazy('admin-panel:qbank-list')

    def get_redirect_url(self, *args, **kwargs):

        pk = kwargs.get('pk')

        item = get_object_or_404(self.model, pk=pk)


        if item.is_active:
            item.is_active = False
            messages.success(self.request, 'سوال غیر فعال شد')
            item.updated_at = None


        else: 
            item.is_active = True
            messages.success(self.request, '  سوال فعال شد و انتشار یافت')
 

        item.save()


        return self.success_url


