
from django.views.generic import  RedirectView, ListView, CreateView, UpdateView
from admin_panel.mixins import AdminPermissionRequire
from user.models import GradeCategories, MajorCategories
from quiz.models import LessionCategories
from django.shortcuts import render, get_object_or_404
from admin_panel.forms.categories import (
    LessionModelForm, 
    GradeModelForm, 
    MajorModelForm,
    PossibleModelForm,
    QuestionPossible, 
    TicketProblemPlacementModelForm,
    TicketProblemCategoryModelForm

)
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from sitesetting.models import TicketProblemPlacement, TicketProblemCategory

# major category
class MajorListView(AdminPermissionRequire, ListView):
    """for list the major categories"""

    context_object_name = 'items'
    template_name = 'admin-panel/categories/major/list.html'
    queryset = MajorCategories.objects.all()
    paginate_by = 200
class MajorCreate(AdminPermissionRequire, CreateView):
    """for create major categories"""

    template_name = 'admin-panel/categories/major/create.html'
    model = MajorCategories
    form_class = MajorModelForm
    success_url = reverse_lazy('admin-panel:categories-major-list')

    def form_valid(self, form):
        messages.success(
            self.request, 'ایتم با موفقیت افزوده شد'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, form.errors
        )
        return super().form_invalid(form)
class MajorUpdate(AdminPermissionRequire, UpdateView):
    """for update major categories"""

    template_name = 'admin-panel/categories/major/create.html'
    model = MajorCategories
    form_class = MajorModelForm
    success_url = reverse_lazy('admin-panel:categories-major-list')

    def form_valid(self, form):
        messages.success(
            self.request, 'ایتم با موفقیت افزوده شد'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, form.errors
        )
        return super().form_invalid(form)
class MajorActiveDeactivate(AdminPermissionRequire, RedirectView):
    """for deactivate or activate the major """

    model = MajorCategories
    success_url = reverse_lazy('admin-panel:categories-major-list')

    def get_redirect_url(self, *args, **kwargs):

        pk = kwargs.get('pk')

        item = get_object_or_404(self.model, pk=pk)


        if item.is_active:
            item.is_active = False
            messages.success(self.request, 'ایتم غیر فعال شد')
        else: 
            item.is_active = True
            messages.success(self.request, 'ایتم فعال شد')
            
        item.save()


        return self.success_url

# major category
class GradeListView(AdminPermissionRequire, ListView):
    """for list the grade categories"""

    context_object_name = 'items'
    template_name = 'admin-panel/categories/grade/list.html'
    queryset = GradeCategories.objects.all()
    paginate_by = 200
class GradeCreate(MajorCreate):
    """for create grade categories"""

    template_name = 'admin-panel/categories/grade/create.html'
    model = GradeCategories
    form_class = GradeModelForm
    success_url = reverse_lazy('admin-panel:categories-grade-list') 
class GradeUpdate(MajorUpdate):
    """for update grade categories"""

    template_name = 'admin-panel/categories/grade/create.html'
    model = GradeCategories
    form_class = GradeModelForm
    success_url = reverse_lazy('admin-panel:categories-grade-list') 
class GradeActiveDeactivate(MajorActiveDeactivate):
    """for deactivate or activate the grade """

    model = GradeCategories
    success_url = reverse_lazy('admin-panel:categories-grade-list')

# possble category
class PossibleListView(AdminPermissionRequire, ListView):
    """for list the possible categories"""

    context_object_name = 'items'
    template_name = 'admin-panel/categories/possible/list.html'
    queryset = QuestionPossible.objects.all()
    paginate_by = 200
class PossibleCreate(MajorCreate):
    """for create possible categories"""

    template_name = 'admin-panel/categories/possible/create.html'
    model = QuestionPossible
    form_class = PossibleModelForm
    success_url = reverse_lazy('admin-panel:categories-possible-list') 
class PossibleUpdate(MajorUpdate):
    """for update possible categories"""

    template_name = 'admin-panel/categories/possible/create.html'
    model = QuestionPossible
    form_class = PossibleModelForm
    success_url = reverse_lazy('admin-panel:categories-possible-list') 
class PossibleActiveDeactivate(MajorActiveDeactivate):
    """for deactivate or activate the possible """

    model = QuestionPossible
    success_url = reverse_lazy('admin-panel:categories-possible-list')

# lession category
class LessionListView(AdminPermissionRequire, ListView):
    """for list the lession categories"""

    context_object_name = 'items'
    template_name = 'admin-panel/categories/lession/list.html'
    queryset = LessionCategories.objects.all()
    paginate_by = 200
class LessionCreate(MajorCreate):
    """for create lession categories"""

    template_name = 'admin-panel/categories/lession/create.html'
    model = LessionCategories
    form_class = LessionModelForm
    success_url = reverse_lazy('admin-panel:categories-lession-list') 
class LessionUpdate(MajorUpdate):
    """for update lession categories"""

    template_name = 'admin-panel/categories/lession/create.html'
    model = LessionCategories
    form_class = LessionModelForm
    success_url = reverse_lazy('admin-panel:categories-lession-list') 
class LessionActiveDeactivate(MajorActiveDeactivate):
    """for deactivate or activate the lession """

    model = LessionCategories
    success_url = reverse_lazy('admin-panel:categories-lession-list')

# problem category of tickets 
class TicketProblemPlacementListView(AdminPermissionRequire, ListView):
    """for list the TicketProblemPlacement"""

    context_object_name = 'items'
    template_name = 'admin-panel/categories/TicketProblemPlacement/list.html'
    queryset = TicketProblemPlacement.objects.all()
    paginate_by = 200
class TicketProblemPlacementCreate(MajorCreate):
    """for create TicketProblemPlacement"""

    template_name = 'admin-panel/categories/TicketProblemPlacement/create.html'
    model = TicketProblemPlacement
    form_class = TicketProblemPlacementModelForm
    success_url = reverse_lazy('admin-panel:categories-TicketProblemPlacement-list') 
class TicketProblemPlacementUpdate(MajorUpdate):
    """for update TicketProblemPlacement"""

    template_name = 'admin-panel/categories/TicketProblemPlacement/create.html'
    model = TicketProblemPlacement
    form_class = TicketProblemPlacementModelForm
    success_url = reverse_lazy('admin-panel:categories-TicketProblemPlacement-list') 
class TicketProblemPlacementActiveDeactivate(MajorActiveDeactivate):
    """for deactivate or activate the TicketProblemPlacement """

    model = TicketProblemPlacement
    success_url = reverse_lazy('admin-panel:categories-TicketProblemPlacement-list')

# problem category of site section for tickets 
class TicketProblemCategoryListView(AdminPermissionRequire, ListView):
    """for list the lession categories"""

    context_object_name = 'items'
    template_name = 'admin-panel/categories/TicketProblemCategory/list.html'
    queryset = TicketProblemCategory.objects.all()
    paginate_by = 200
class TicketProblemCategoryCreate(MajorCreate):
    """for create lession categories"""

    template_name = 'admin-panel/categories/TicketProblemCategory/create.html'
    model = TicketProblemCategory
    form_class = TicketProblemCategoryModelForm
    success_url = reverse_lazy('admin-panel:categories-TicketProblemCategory-list') 
class TicketProblemCategoryUpdate(MajorUpdate):
    """for update lession categories"""

    template_name = 'admin-panel/categories/TicketProblemCategory/create.html'
    model = TicketProblemCategory
    form_class = TicketProblemCategoryModelForm
    success_url = reverse_lazy('admin-panel:categories-TicketProblemCategory-list') 
class TicketProblemCategoryActiveDeactivate(MajorActiveDeactivate):
    """for deactivate or activate the lession """

    model = TicketProblemCategory
    success_url = reverse_lazy('admin-panel:categories-TicketProblemCategory-list')


 

