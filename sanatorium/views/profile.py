from django.views.generic import TemplateView

class SanatoriumPanel(TemplateView):
    template_name =  'sanatorium/profile/01-dashboard.html'
class SanatoriumPanel1(TemplateView):
    template_name =  'sanatorium/profile/02-account.html'
class SanatoriumPanel2(TemplateView):
    template_name =  'sanatorium/quiz-history/07-exam-history.html'
class SanatoriumPanel3(TemplateView):
    template_name =  'sanatorium/quiz-history/07b-exam-history-detail copy.html'
class SanatoriumPanel4(TemplateView):
    template_name =  'sanatorium/quiz-remain/08-pending-exams.html'
class SanatoriumPanel5(TemplateView):
    template_name =  'sanatorium/quiz-remain/09-students-list.html'
class SanatoriumPanel6(TemplateView):
    template_name =  'sanatorium/quiz-remain/10-exam-questions.html'
class SanatoriumPanel7(TemplateView):
    template_name =  'sanatorium/quiz-remain/11-question-detail.html'
class SanatoriumPanel8(TemplateView):
    template_name =  'sanatorium/tickets/03-tickets-list.html'
class SanatoriumPanel9(TemplateView):
    template_name =  'sanatorium/tickets/04-send-ticket.html'
class SanatoriumPanel10(TemplateView):
    template_name =  'sanatorium/tickets/05-ticket-conversation.html'
    