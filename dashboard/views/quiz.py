from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from quiz.models import Quiz, Question, StudentAnswer, QuestionAnswerKey
from django.db.models import Q
from django.db.models.aggregates import Count
from django.http import Http404

class QuizList(LoginRequiredMixin, ListView):
    template_name = 'dashboard/quiz/07-exam-list.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = Quiz.objects.filter(
            student=self.request.user,
            is_active=True,   
        ).prefetch_related('grade', 'major', 'lession'
        ).annotate(question_count=Count('questions'))
        return queryset
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['status'] = Quiz.QuizStatus
        return data
    
class QuizDetail(LoginRequiredMixin, ListView):
    template_name = 'dashboard/quiz/08-exam-detail.html'
    context_object_name = 'items'

    def get_queryset(self):
        self.quiz = Quiz.objects.filter(
            student=self.request.user,
            is_active=True,
            pk=self.kwargs.get('pk')   
        )

        if not self.quiz.exists() or self.quiz.count() != 1 :
            raise Http404
        

        self.quiz = self.quiz.prefetch_related('grade', 'major', 'lession', 'questions', 'reports', 'student_answers').first()
        self.questions = self.quiz.questions.filter(is_active=True).prefetch_related('student_answers', 'answer_key', 'options')

        return self.questions 
        
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['TypeOfQuestions'] = Question.TypeOfQuestions
        data['TypeOfKey'] = QuestionAnswerKey.TypeOfAnswer
        data['status'] = Quiz.QuizStatus
        data['corrected'] = StudentAnswer.TypeOfCorrect
        data['TypeOfAnswer'] = StudentAnswer.TypeOfAnswer
        data['quiz'] = self.quiz
        data['answers'] = self.quiz.student_answers.all()
        data['report'] = self.quiz.reports.filter(user=self.request.user).first()

        question_user = self.questions.filter(student_answers__student=self.request.user)

        data['not_corrected'] = question_user.filter(student_answers__corrected=StudentAnswer.TypeOfCorrect.not_corrected).count()
        data['skipped'] = question_user.filter(Q(student_answers__is_skipped=True) | Q(student_answers__type_of_answer__isnull=True) ).count()
        data['excellent'] = question_user.filter(student_answers__corrected=StudentAnswer.TypeOfCorrect.excellent, ).count()
        data['good'] = question_user.filter(student_answers__corrected=StudentAnswer.TypeOfCorrect.good, ).count()
        data['average'] = question_user.filter(student_answers__corrected=StudentAnswer.TypeOfCorrect.average, ).count()
        data['weak'] =question_user.filter(student_answers__corrected=StudentAnswer.TypeOfCorrect.weak, ).count()
        data['wrong'] = question_user.filter(student_answers__corrected=StudentAnswer.TypeOfCorrect.wrong, ).count()

        return data
    
