from django.views.generic import TemplateView



class QuizList(TemplateView):
    template_name = 'dashboard/quiz/07-exam-list.html'


class QuizDetail(TemplateView):
    template_name = 'dashboard/quiz/08-exam-detail.html'

