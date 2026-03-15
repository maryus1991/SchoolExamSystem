from django.views.generic import TemplateView


class SanatoriumPendingExamList(TemplateView):
    template_name =  'sanatorium/quiz-remain/08-pending-exams.html'

class SanatoriumStudentListOfExam(TemplateView):
    template_name =  'sanatorium/quiz-remain/09-students-list.html'
    
class SanatoriumQuestionListPerStudentOfExam(TemplateView):
    template_name =  'sanatorium/quiz-remain/10-exam-questions.html'

class SanatoriumQuestionDetailPerStudentOfExam(TemplateView):
    template_name =  'sanatorium/quiz-remain/11-question-detail.html'