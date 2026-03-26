from admin_panel.mixins import AdminPermissionRequire
from sitesetting.models import Ticket, TicketChat
from django.views.generic import View, ListView
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.http import Http404
from admin_panel.forms.tickers import TicketChatForm
from django.contrib import messages

class TicketListViews(AdminPermissionRequire, ListView):
    """ for list the tickets """

    template_name = 'admin-panel/tickets/list.html'
    context_object_name = 'items'
 
    paginate_by = 50


    def get_queryset(self):
        return Ticket.objects.prefetch_related('user', 'problem', 'placement') 
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['priority'] = Ticket.TicketPriority
        data['status'] = Ticket.TicketStatus
        data['await_response'] = self.get_queryset().filter(Q(status=Ticket.TicketStatus.awating_user) | Q(status=Ticket.TicketStatus.awating_admin)).count()
        data['closed'] = self.get_queryset().filter(Q(status=Ticket.TicketStatus.fixed) | Q(status=Ticket.TicketStatus.cancelled)).count()

        return data
    
class TicketChat(AdminPermissionRequire, View):
    """chat in ticket"""
    template_name = 'admin-panel/tickets/chat.html'

    def get(self, request , *args, **kwargs):
        
        item = Ticket.objects.filter(
            pk=kwargs.get('pk'), 
            ).prefetch_related('chats')

        if not item.exists() or item.count() != 1:
            raise Http404()
        
        item = item.last()

        # for chat in item.chats.filter(is_read_by_admin=False).all():
        #     chat.is_read_by_admin = True
        #     chat.save()
        item.chats.filter(is_read_by_admin=False).update(is_read_by_admin = True)

        context={
            'item': item,
            'chats': item.chats.all(),
            'form': TicketChatForm(),
            'priority' : Ticket.TicketPriority,
            'status' : Ticket.TicketStatus,
        }

        return render(request, self.template_name, context)

    def post(self, request , *args, **kwargs):


        messages.success(request, 'پیام شما ارسال شد')
        item = Ticket.objects.filter(
            user=request.user, 
            pk=kwargs.get('pk'), 
        ).prefetch_related('chats')

        if not item.exists() or item.count() != 1:
            raise Http404()
        
        item = item.last()

        form = TicketChatForm(request.POST or None)
        if form.is_valid():
            item.chats.create(
                is_read_by_admin=True,
                admin_message=form.cleaned_data.get('message'),
                is_admin_message=True
            )
            messages.success(request, 'پیام شما ارسال شد')
            item.status = Ticket.TicketStatus.awating_user
            item.admin = request.user 
            item.save()

        else:
            messages.error(request, form.errors)

        return self.get(request, *args, **kwargs)

