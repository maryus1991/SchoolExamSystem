from django.views.generic import TemplateView, ListView, View
from quiz.models import Quiz, StudentAnswer
from sanatorium.mixins import SanatorPermissionRequire
from django.db.models import Q
from django.db.models.aggregates import Count
from django.shortcuts import render


class SanatoriumPendingExamList(SanatorPermissionRequire, ListView):
    template_name =  'sanatorium/quiz-remain/08-pending-exams.html'
    context_object_name = 'items'

    def get_queryset(self):
        self.queryset = Quiz.objects.filter(sanatorium=self.request.user, is_active=True).prefetch_related('grade', 'major', 'lession').annotate(
            question_count=Count('questions'),
            student_count=Count('detail'),
        ).order_by('-pk')
        return self.queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['status'] = Quiz.QuizStatus
        data['corrected'] = self.queryset.filter(
            Q(status=Quiz.QuizStatus.CORRECTED) |
            Q(status=Quiz.QuizStatus.RESULTS_PUBLISHED) 
        ).count()
        data['wait_corrected'] = self.queryset.filter(
            Q(status=Quiz.QuizStatus.FINISHED) |
            Q(status=Quiz.QuizStatus.WAITING_CORRECTION) 
        ).count()


        return data

class SanatoriumStudentListOfExam(SanatorPermissionRequire, TemplateView):
    template_name =  'sanatorium/quiz-remain/09-students-list.html'
    
class SanatoriumQuestionListPerStudentOfExam(SanatorPermissionRequire, TemplateView):
    template_name =  'sanatorium/quiz-remain/10-exam-questions.html'

class SanatoriumQuestionDetailPerStudentOfExam(SanatorPermissionRequire, View):
    template_name =  'sanatorium/quiz-remain/11-question-detail.html'

    def get(cls, request, *args, **kwargs):
        return render(request, cls.template_name)

    def post(cls, request, *args, **kwargs):
        pass
