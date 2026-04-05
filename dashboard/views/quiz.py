from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from quiz.models import Quiz, Question, StudentAnswer, QuestionAnswerKey
from django.db.models import Q
from django.db.models.aggregates import Count
from django.http import Http404

class QuizList(LoginRequiredMixin, ListView):
    template_name = 'dashboard/quiz/07-exam-list.html'
    context_object_name = 'items'
    paginate_by = 50

    def get_queryset(self):
        queryset = Quiz.objects.filter(
            student=self.request.user,
            is_active=True,   
        ).prefetch_related('grade', 'major', 'lession'
        ).annotate(question_count=Count('questions'))
        return queryset.order_by('-pk')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['status'] = Quiz.QuizStatus
        return data
    
    
class QuizDetail(LoginRequiredMixin, ListView):
    template_name = 'dashboard/quiz/08-exam-detail.html'
    context_object_name = 'answers'
    paginate_by = 10


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
        self.answers = self.quiz.student_answers.prefetch_related('question').filter(student=self.request.user).all()
        return self.answers
        
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        data['TypeOfQuestions'] = Question.TypeOfQuestions
        data['TypeOfKey'] =       QuestionAnswerKey.TypeOfAnswer
        data['status'] =          Quiz.QuizStatus
        data['corrected'] =       StudentAnswer.TypeOfCorrect
        data['TypeOfAnswer'] =    StudentAnswer.TypeOfAnswer
        data['quiz'] =            self.quiz
             
        data['report'] =          self.quiz.reports.filter(user=self.request.user).first()

        anwers = self.answers

        data['not_corrected'] = anwers.filter(corrected=StudentAnswer.TypeOfCorrect.not_corrected).count()
        data['skipped'] =       anwers.filter(is_skipped=True).count()
        data['excellent'] =     anwers.filter(corrected=StudentAnswer.TypeOfCorrect.excellent, ).count()
        data['good'] =          anwers.filter(corrected=StudentAnswer.TypeOfCorrect.good, ).count()
        data['average'] =       anwers.filter(corrected=StudentAnswer.TypeOfCorrect.average, ).count()
        data['weak'] =          anwers.filter(corrected=StudentAnswer.TypeOfCorrect.weak, ).count()
        data['wrong'] =         anwers.filter(corrected=StudentAnswer.TypeOfCorrect.wrong, ).count()

        return data
    
