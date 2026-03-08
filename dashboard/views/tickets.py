from django.views.generic import TemplateView, ListView, View, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from sitesetting.models import Ticket
from dashboard.forms import TicketForm, TicketChatForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import Http404

class Ticketlist(LoginRequiredMixin, ListView):
    """ticket list"""
    template_name = 'dashboard/tickets/12-ticket-list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Ticket.objects.prefetch_related('placement', 'problem').filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['priority'] = Ticket.TicketPriority
        data['status'] = Ticket.TicketStatus
        data['await_response'] = self.get_queryset().filter(Q(status=Ticket.TicketStatus.awating_user) | Q(status=Ticket.TicketStatus.awating_admin)).count()
        data['closed'] = self.get_queryset().filter(Q(status=Ticket.TicketStatus.fixed) | Q(status=Ticket.TicketStatus.cancelled)).count()

        return data
    

class TicketSend(LoginRequiredMixin, View):
    """send ticket"""
    template_name = 'dashboard/tickets/13-ticket-send.html'

    def get(self, request, *args, **kwargs):
        
        context = {
            'form':TicketForm(request.POST or None),
        }

        return render(request, self.template_name, context)
    
    def post(self, request , *args, **kwargs):
        form = TicketForm(request.POST , request.FILES)

        if form.is_valid():
 
            Ticket.objects.create(
                name=form.cleaned_data.get('name'),
                problem=form.cleaned_data.get('problem'),
                placement=form.cleaned_data.get('placement'),
                description=form.cleaned_data.get('description'),
                file=form.cleaned_data.get('file'),
                priority=form.cleaned_data.get('priority'),
                status=Ticket.TicketStatus.awating_admin,
                user = request.user
                
            )


            messages.success(
                request, 'پیام شما ارسال شد'
            )
            return redirect('dashboard:ticket-list')

        else:
            messages.error(
                request, form.errors
            )

        return self.get(request, *args, **kwargs)

class TicketChat(LoginRequiredMixin, View):
    """chat in ticket"""
    template_name = 'dashboard/tickets/14-ticket-chat.html'

    def get(self, request , *args, **kwargs):
        
        item = Ticket.objects.filter(
            user=request.user, 
            pk=kwargs.get('pk'), 
            ).prefetch_related('chats')

        if not item.exists() or item.count() != 1:
            raise Http404()
        
        item = item.last()

        for chat in item.chats.filter(is_read_by_user=False).all():
            chat.is_read_by_user = True
            chat.save()

        context={
            'item': item,
            'chats': item.chats.all(),
            'form': TicketChatForm(),
            'priority' : Ticket.TicketPriority,
            'status' : Ticket.TicketStatus,
        }

        return render(request, self.template_name, context)

    def post(self, request , *args, **kwargs):

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
                is_read_by_user=True,
                user_message=form.cleaned_data.get('message')
            )
            messages.success(request, 'پیام شما ارسال شد')
            
        else:
            messages.error(request, form.errors)

        return self.get(request, *args, **kwargs)



class TicketCancelled(LoginRequiredMixin, RedirectView):
    """cancel the ticket"""
    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = get_object_or_404(Ticket, pk=pk, user=self.request.user)
        obj.status = Ticket.TicketStatus.cancelled
        obj.save()
        messages.info(
            self.request, 'تیکت کنسل شد'
        )

        return obj.get_absolute_url()


class TicketFixed(LoginRequiredMixin, RedirectView):
    """set fixed status for the ticket"""
    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = get_object_or_404(Ticket, pk=pk, user=self.request.user)
        obj.status = Ticket.TicketStatus.fixed
        obj.save()
        messages.success(
            self.request, 'تیکت بسته شد'
        )

        return obj.get_absolute_url()