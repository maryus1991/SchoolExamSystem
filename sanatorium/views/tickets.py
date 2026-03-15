from django.views.generic import TemplateView
from dashboard.views.tickets import Ticketlist, TicketSend, TicketChat

class TicketList(Ticketlist):
    template_name =  'sanatorium/tickets/03-tickets-list.html'

class SendTicket(TicketSend):
    template_name =  'sanatorium/tickets/04-send-ticket.html'

class TicketConversation(TicketChat):
    template_name =  'sanatorium/tickets/05-ticket-conversation.html'
    