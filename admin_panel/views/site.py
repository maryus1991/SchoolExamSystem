from django.views.generic import TemplateView, UpdateView, CreateView, ListView, View
from admin_panel.forms.site import SiteModelForm, SiteLawModelForm, TeamModelForm, QuestionAndAnswerModelForm
from django.contrib import messages
from admin_panel.mixins import AdminPermissionRequire
from sitesetting.models import Site, Team, QuestionAndAnswer, SiteLaw
from django.urls import reverse_lazy
from user.models import User
from sitesetting.models import Ticket
from order.models import Order
from quiz.models import Quiz
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotAllowed
from django.core.management import call_command
from django.utils.timezone import timedelta, now    
import io
 

class DownloadDatabaseBackupView(AdminPermissionRequire, View):
 
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed('شما اجازه دانلود ندارید')
    

    def get(self, request, *args, **kwargs):
        # ایجاد یک فایل متنی موقت در حافظه (RAM)
        output = io.StringIO()
        
        try:
            # فراخوانی دستور dumpdata جنگو
            # جداول لاگ‌ها، سشن‌ها و پرمیژن‌ها را حذف می‌کنیم تا موقع ری‌استور ارور ندهد
            call_command(
                'dumpdata',
                format='json',
                indent=2,
                exclude=['contenttypes', 'auth.permission', 'admin.logentry', 'sessions.session'],
                stdout=output
            )
            
            # برگرداندن نشانگر به ابتدای فایل
            output.seek(0)
            
            # آماده‌سازی فایل برای دانلود
            response = HttpResponse(output.read(), content_type='application/json')
            
            # تولید نام فایل بر اساس تاریخ و ساعت فعلی
            filename = f"db_backup_{now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response
            
        except Exception as e:
            return HttpResponse(f"خطا در تهیه بکاپ: {str(e)}", status=500)
        finally:
            output.close()

class Main(TemplateView):
    template_name = 'admin-panel/main.html'

    def get_context_data(self, **kwargs) -> dict[str, ...]:
        context = super().get_context_data(**kwargs)
        quiz = Quiz.objects
        context['quiz_count'] = quiz.count() 
        context['quiz_list'] = quiz.order_by('-pk').all()[:4]

        users = User.objects
        orders = Order.objects.filter(update_at__gte=now() - timedelta(days=30))
        
        context['users_count'] = users.count()
        context['last_users'] = users.order_by('-pk').all()[:4]


        context['orders_list'] = orders.prefetch_related('user').all()[:4]
        context['order_count'] = orders.count()
        context['all_order_count'] = orders.count()
        context['active_order_count'] = orders.filter(status=Order.OrderStatus.active).count()
        context['active_order_percent'] = round( 
                (context['active_order_count'] / context['all_order_count']) * 100
             )
        context['paid_order_count'] = orders.filter(status=Order.OrderStatus.paid).count()
        context['paid_order_percent'] =  round( 
                (context['paid_order_count'] / context['all_order_count']) * 100
             )
        context['cancell_order_count'] = orders.filter(
            Q(status=Order.OrderStatus.cancelled_by_admin) | Q(status=Order.OrderStatus.cancelled)
        ).count()
        context['cancell_order_percent'] = round( 
                (context['cancell_order_count'] / context['all_order_count']) * 100
             )
        context['all_peyment_for_last_month'] = sum(
            orders.values_list('final_price', flat=True)
        )


        context['last_tickets'] = Ticket.objects.order_by('-pk').prefetch_related('user').all()[:4]


        return context
    
class SiteUpdateView(AdminPermissionRequire, UpdateView):
    """for update the site settings """

    context_object_name = 'item'
    template_name = 'admin-panel/settings/index.html'
    form_class = SiteModelForm
    success_url = reverse_lazy('admin-panel:site')

    def get_object(self):
        return Site.objects.first()

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'تغییرات اعمال شد')
        return super().form_valid(form)
    
# team 
class TeamListView(AdminPermissionRequire, ListView):
    """list view for team"""

    queryset = Team.objects.all()
    context_object_name = 'items'
    template_name = 'admin-panel/settings/team/list.html'
    paginate_by = 100
class TeamCreateView(AdminPermissionRequire, CreateView):
 
    queryset = Team.objects.all()
    context_object_name = 'items'
    template_name = 'admin-panel/settings/team/create.html'
    form_class = TeamModelForm
    success_url = reverse_lazy('admin-panel:site-team-list')

    def form_valid(self, form):
        messages.success(self.request, 'ایتم اضافه شد')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
class TeamUpdateView(AdminPermissionRequire, UpdateView):
 
    queryset = Team.objects.all()
    context_object_name = 'items'
    template_name = 'admin-panel/settings/team/create.html'
    form_class = TeamModelForm
    success_url = reverse_lazy('admin-panel:site-team-list')


    def form_valid(self, form):
        messages.success(self.request, 'ایتم اضافه شد')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

# Q&A    
class QuestionAndAnswerListView(AdminPermissionRequire, ListView):
    """list view for QuestionAndAnswer"""

    queryset = QuestionAndAnswer.objects.all()
    context_object_name = 'items'
    template_name = 'admin-panel/settings/Q&A/list.html'
    paginate_by = 100
class QuestionAndAnswerCreateView(TeamCreateView):
  
    context_object_name = 'items'
    template_name = 'admin-panel/settings/Q&A/create.html'
    form_class = QuestionAndAnswerModelForm
    success_url = reverse_lazy('admin-panel:site-qa-list')
class QuestionAndAnswerUpdateView(TeamUpdateView):
 

    queryset = QuestionAndAnswer.objects.all()
    context_object_name = 'items'
    template_name = 'admin-panel/settings/Q&A/create.html'
    form_class = QuestionAndAnswerModelForm
    success_url = reverse_lazy('admin-panel:site-qa-list')


# site law
class SiteLawListView(AdminPermissionRequire, ListView):
    """list view for SiteLaw"""

    queryset = SiteLaw.objects.all()
    context_object_name = 'items'
    template_name = 'admin-panel/settings/law/list.html'
    paginate_by = 100
class SiteLawCreateView(TeamCreateView):
  
    context_object_name = 'items'
    template_name = 'admin-panel/settings/law/create.html'
    form_class = SiteLawModelForm
    success_url = reverse_lazy('admin-panel:site-law-list')
class SiteLawUpdateView(TeamUpdateView):
 

    queryset = SiteLaw.objects.all()
    context_object_name = 'items'
    template_name = 'admin-panel/settings/law/create.html'
    form_class = SiteLawModelForm
    success_url = reverse_lazy('admin-panel:site-law-list')



    