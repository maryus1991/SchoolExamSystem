
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from qbank.models import QuestionLessonCategory
from quiz.models import LessionCategories

class FavorateQuestionList(LoginRequiredMixin, ListView):
    template_name = 'dashboard/favorate/09-question-list.html'
    context_object_name = 'items'
    paginate_by = 50

    def get_queryset(self):
        return self.request.user.favorate.qbank.filter(is_active=True).prefetch_related('category', 'possible').all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cagegories'] = QuestionLessonCategory.objects.filter(is_active=True).all()
        return data

class FavorateBlogList(LoginRequiredMixin, ListView):
    template_name = 'dashboard/favorate/09-blog-list.html'
    context_object_name = 'items'
    paginate_by = 50


    
    def get_queryset(self):
        return self.request.user.favorate.blog.filter(is_active=True).all()


class FavorateQuizList(LoginRequiredMixin, ListView):
    template_name = 'dashboard/favorate/09-quiz-list.html'
    context_object_name = 'items'
    paginate_by = 50


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cagegories'] = LessionCategories.objects.filter(is_active=True).all()
        return data
        
    def get_queryset(self):
        return self.request.user.favorate.quiz.filter(is_active=True).prefetch_related('grade').all()

 