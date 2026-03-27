from django.views.generic import CreateView, ListView, RedirectView, View, UpdateView
from django.contrib import messages 
from qbank.models import QuestionBank, QuestionOption, QuestionAnswerKey
from admin_panel.mixins import AdminPermissionRequire
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from admin_panel.forms.qbank import QuestionAnwerKeyModelForm, QuestionOptionsModelForm, QuestionBankModelForm

class QuestionBankListView(AdminPermissionRequire, ListView):
    """for list the questions"""

    context_object_name = 'items'
    template_name = 'admin-panel/question-bank/list.html'
    queryset = QuestionBank.objects.prefetch_related('possible', 'category').all()
    paginate_by = 250

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

# create

class QbankCreateView(AdminPermissionRequire, CreateView):
    """ for create new question """

    form_class = QuestionBankModelForm
    model = QuestionBank.objects.prefetch_related('options')
    template_name = 'admin-panel/question-bank/create-question.html'
    
    def get_success_url(self):

        messages.success(self.request, 'سوال ساخته شد')
        item: QuestionBank = self.object

        if (item.has_options or 
            item.type_of_question == QuestionBank.TypeOfQuestions.MULTIPLE_CHOICE 
            or item.type_of_question == QuestionBank.TypeOfQuestions.TRUE_FALSE   ) and not item.options.all():

            if not item.has_options: 
                item.has_options = True
                item.save()

            return reverse_lazy('admin-panel:qbank-create-option', kwargs={'pk':item.pk})
        
        if QuestionAnswerKey.objects.get_or_create(question=item)[1] :
            return reverse_lazy('admin-panel:qbank-create-key', kwargs={'pk':item.pk})
        
        return reverse_lazy('admin-panel:qbank-update', kwargs={'pk':item.pk})

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

class QbankOptionCreate(AdminPermissionRequire, CreateView):
    """for create option for question"""
    
    form_class = QuestionOptionsModelForm
    model = QuestionOption
    template_name = 'admin-panel/question-bank/create-options.html'

    def dispatch(self, request, *args, **kwargs):
        self.item = get_object_or_404(QuestionBank, pk=self.kwargs.get('pk')) 
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.question = self.item 
        return super().form_valid(form)
    
    def get_success_url(self):
     
        messages.success(self.request, 'گزینه به سوال مورد نظر افزوده شد')   

        if '_addanother' in self.request.POST:
            return reverse_lazy('admin-panel:qbank-create-option', kwargs={'pk':self.item.pk})
        
        if QuestionAnswerKey.objects.get_or_create(question=self.item)[1] :
            return reverse_lazy('admin-panel:qbank-create-key', kwargs={'pk':self.item.pk})
        
        else:
            return reverse_lazy('admin-panel:qbank-update', kwargs={'pk':self.item.pk})

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['item'] = self.item
        return data 

class QbankAnswerKey(AdminPermissionRequire, CreateView):
    """for create key for question"""
    
    form_class = QuestionAnwerKeyModelForm
    model = QuestionAnswerKey
    template_name = 'admin-panel/question-bank/create-key.html'

    def dispatch(self, request, *args, **kwargs):
        self.item = get_object_or_404(QuestionBank, pk=self.kwargs.get('pk')) 
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'کلید ذخیره شد')
        form.instance.question = self.item 

        QuestionAnswerKey.objects.filter(question=self.item).delete()
 
        return super().form_valid(form)
        
    
    def get_success_url(self):
        return reverse_lazy('admin-panel:qbank-update', kwargs={'pk':self.item.pk})

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['item'] = self.item
        return data 

# update

class QbankUpdateView(AdminPermissionRequire, UpdateView):
    """ for update question """

    form_class = QuestionBankModelForm
    template_name = 'admin-panel/question-bank/create-question.html'
    context_object_name = 'item'
    

    def get_queryset(self):
        return QuestionBank.objects.prefetch_related('options', 'answer_key')
         
    
    def get_success_url(self):

        messages.success(self.request, 'سوال بروز رسانی شد')
        item: QuestionBank = self.get_object()

        return reverse_lazy('admin-panel:qbank-create-key', kwargs={'pk':item.pk})

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
class QbankOptionUpdateView(AdminPermissionRequire, UpdateView):
    """for update option for question"""
    
    form_class = QuestionOptionsModelForm
    model = QuestionOption
    template_name = 'admin-panel/question-bank/create-options.html'
    
    def get_success_url(self):
        return reverse_lazy('admin-panel:qbank-update', kwargs={'pk': self.get_object().question.pk})

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['item'] = self.get_object().question
        return data 

class QbankAnswerKeyUpdateView(AdminPermissionRequire, UpdateView):
    """for create key for question"""
    
    form_class = QuestionAnwerKeyModelForm
    template_name = 'admin-panel/question-bank/create-key.html'

    def get_object(self):
        self.item = get_object_or_404(QuestionBank, pk=self.kwargs.get('pk')) 
        return QuestionAnswerKey.objects.get_or_create(question=self.item)[0]

    def form_valid(self, form):
        messages.success(self.request, 'کلید بروز رسانی شد')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('admin-panel:qbank-update', kwargs={'pk':self.item.pk})

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['item'] = self.item
        return data 

# delete

class QuestionOptionDelete(AdminPermissionRequire, RedirectView):
    """for delete the option"""

    def get_redirect_url(self, *args, **kwargs):

        pk = kwargs.get('pk')
        item = get_object_or_404(QuestionOption, pk=pk)
        item.delete()
        messages.info(self.request, 'گزینه حذف شد')

        return reverse_lazy('admin-panel:qbank-update', kwargs={'pk':item.question.pk})

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
