from django.views.generic import CreateView, UpdateView, RedirectView, ListView, View
from admin_panel.mixins import AdminPermissionRequire
from quiz.models import Quiz, QuestionOption, Question, QuestionAnswerKey, UserQuizDetail
from admin_panel.forms.quiz import QuizModelForm, QuestionModelForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count

class QuizListView(AdminPermissionRequire, ListView):
    """for list the exams"""

    template_name = 'admin-panel/exam/quiz/list.html'
    context_object_name = 'items'
    paginate_by = 25
    queryset = Quiz.objects.prefetch_related(
        'grade', 'major' ,'lession', 'questions'
        ).annotate(student_count=Count('student')).all()
class QuizCreateView(AdminPermissionRequire, CreateView):
    """for create quiz"""

    form_class = QuizModelForm
    template_name = 'admin-panel/exam/quiz/create.html'
    success_url = reverse_lazy('admin-panel:quiz-list')

    def form_valid(self, form):
        messages.success(self.request, 'ایتم ساخته شد')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
class QuizUpdateView(AdminPermissionRequire, UpdateView):
    """for update quiz"""

    form_class = QuizModelForm
    template_name = 'admin-panel/exam/quiz/create.html'
    success_url = reverse_lazy('admin-panel:quiz-list')
    context_object_name = 'item'
    model = Quiz


    def form_valid(self, form):
        messages.success(self.request, 'ایتم بروز رسانی شد')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
class QuizActivateView(AdminPermissionRequire, RedirectView):
    """for active or deactivated the quiz"""

    def get_redirect_url(self, *args, **kwargs):

        item = get_object_or_404(Quiz, pk=kwargs.get('pk'))

        if item.is_active:
            messages.info(self.request, 'ایتم غیر فعال شد')
            item.is_active = False
            item.save()
        else:
            messages.info(self.request, 'ایتم فعال شد')
            item.is_active = True
            item.save()

        return reverse_lazy('admin-panel:quiz-list')
class QuizStartCurrectingView(AdminPermissionRequire, RedirectView):
    """for start currecting the quiz"""

    def get_redirect_url(self, *args, **kwargs):

        item = get_object_or_404(Quiz, pk=kwargs.get('pk'))

       
 
        if item.status == Quiz.QuizStatus.FINISHED:
            item.start_set_report = False
            item.status = Quiz.QuizStatus.WAITING_CORRECTION
            item.save()
            messages.warning(self.request, 'تصحیح شروع شد')
        else:
            messages.warning(self.request, 'این ازمون به مرحله تمام نرسیده است')

        return reverse_lazy('admin-panel:quiz-list')


class QuestionListView(AdminPermissionRequire, ListView):
    """for list the questions of quiz"""

    template_name = 'admin-panel/exam/questions/list.html'
    context_object_name = 'items'

    def get_queryset(self):
 
        self.quiz = get_object_or_404(Quiz, pk=self.kwargs.get('quiz_id'))
 
        return self.quiz.questions.all()
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['quiz'] = self.quiz
        return data
class QuestionCreateView(AdminPermissionRequire, CreateView):
    """for create question for quiz"""
    
    model = Question.objects.prefetch_related('options')
    template_name = 'admin-panel/exam/questions/create-question.html'
    form_class = QuestionModelForm

    def form_valid(self, form):
        type_of_question = form.cleaned_data.get('type_of_answer')
 
        if type_of_question == Question.TypeOfQuestions.LONG_ANSWER and not form.cleaned_data.get('description'):
            messages.error(self.request, 'لطفا توضیحات را ثبت کنید')
            return self.form_invalid(form)
        elif type_of_question == Question.TypeOfQuestions.SHORT_ANSWER and not form.cleaned_data.get('description'):
            messages.error(self.request, 'لطفا توضیحات را ثبت کنید')
            return self.form_invalid(form)
        elif type_of_question == Question.TypeOfQuestions.IMAGE_BASED and not form.cleaned_data.get('image'):
            messages.error(self.request, 'لطفا عکس را اپلود کنید')
            return self.form_invalid(form)
        elif type_of_question == Question.TypeOfQuestions.PDF_BASED and not form.cleaned_data.get('pdf_file'):
            messages.error(self.request, 'لطفا فایل pdf را وارد کنید')
            return self.form_invalid(form)
    
        form.instance.quiz = get_object_or_404(Quiz, pk=self.kwargs.get('quiz_id'))

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['status'] = Question.TypeOfQuestions 

        return data
    
    def get_success_url(self):
        messages.success(self.request, 'سوال افزوده شد')
        return reverse_lazy('admin-panel:qbank-update', kwargs={'pk':self.object.pk})

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class QuestionUpdateView(AdminPermissionRequire, UpdateView):pass


class QuestionAnswerKeyListView(AdminPermissionRequire, ListView):pass
class QuestionAnswerKeyCreateView(AdminPermissionRequire, CreateView):pass
class QuestionAnswerKeyUpdateView(AdminPermissionRequire, UpdateView):pass


class QuestionOptionsListView(AdminPermissionRequire, ListView):pass
class QuestionOptionsCreateView(AdminPermissionRequire, CreateView):pass
class QuestionOptionsUpdateView(AdminPermissionRequire, UpdateView):pass

 