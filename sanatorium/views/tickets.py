from dashboard.views.tickets import Ticketlist, TicketSend, TicketChat
from sanatorium.mixins import SanatorPermissionRequire

class TicketList(SanatorPermissionRequire, Ticketlist):
    template_name =  'sanatorium/tickets/03-tickets-list.html'
    paginate_by = 50


class SendTicket(SanatorPermissionRequire, TicketSend):
    template_name =  'sanatorium/tickets/04-send-ticket.html'

class TicketConversation(SanatorPermissionRequire, TicketChat):
    template_name =  'sanatorium/tickets/05-ticket-conversation.html'
    