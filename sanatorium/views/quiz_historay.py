
from django.views.generic import TemplateView



class SanatoriumExamHistoryList(TemplateView):
    template_name =  'sanatorium/quiz-history/07-exam-history.html'
class SanatoriumExamHistoryDetail(TemplateView):
    template_name =  'sanatorium/quiz-history/07b-exam-history-detail copy.html'