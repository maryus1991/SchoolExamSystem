from django.views.generic import TemplateView


class Ticketlist(TemplateView):
    template_name = 'dashboard/tickets/12-ticket-list.html'

class TicketSend(TemplateView):
    template_name = 'dashboard/tickets/13-ticket-send.html'

class TicketChat(TemplateView):
    template_name = 'dashboard/tickets/14-ticket-chat.html'
