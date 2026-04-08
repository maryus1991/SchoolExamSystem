from django.views.generic import CreateView, UpdateView, RedirectView, ListView, View
from admin_panel.mixins import AdminPermissionRequire
from quiz.models import Quiz, QuestionOption, Question, QuestionAnswerKey, StudentAnswer, User, UserQuizDetail
from admin_panel.forms.quiz import QuizModelForm, QuestionModelForm, QuestionAnwerKeyModelForm, QuestionOptionsModelForm, StudentAnswerModelForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, get_list_or_404
from django.db.models.aggregates import Count
from django.db.models import Q


class AddGrouplyUsersToQuiz(AdminPermissionRequire, ListView):
    """for add users to quiz"""

    model = User
    paginate_by = 250
    template_name = 'admin-panel/exam/users/list.html'
    context_object_name = 'items'
    ordering = '-id'

    def dispatch(self, request, *args, **kwargs):
        self.quiz : Quiz = get_object_or_404(Quiz.objects.prefetch_related('student'), pk=kwargs.get('quiz_id'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, ...]:
        context = super().get_context_data(**kwargs)
        context["quiz"] = self.quiz 
        context["type"] = User.TypeOfUser 
        return context

    def post(self, request, *args, **kwargs):
        if 'add' in request.POST:
            users = request.POST.getlist('users')
            users = User.objects.filter(id__in=users)
            self.quiz.student.add(*users)

            for user in users:
                UserQuizDetail.objects.get_or_create(
                    quiz = self.quiz,
                    student=user
                )


            messages.success(request, f'{users.count()} کاربر به ازمون اضافه شدن ')

        if 'remove' in request.POST:
            removed_users = request.POST.getlist('remove_users')
            removed_users = User.objects.filter(id__in=removed_users)
            self.quiz.student.remove(*removed_users)

            messages.error(request, f'{removed_users.count()} کاربر از ازمون حذف شدن ')

        return self.get(request, *args, **kwargs)


class QuizListView(AdminPermissionRequire, ListView):
    """for list the exams"""

    template_name = 'admin-panel/exam/quiz/list.html'
    context_object_name = 'items'
    paginate_by = 25
    queryset = Quiz.objects.prefetch_related(
        'grade', 'major' ,'lession', 'questions'
        ).annotate(student_count=Count('student')).order_by('-pk').all()
class QuizCreateView(AdminPermissionRequire, CreateView):
    """for create quiz"""

    form_class = QuizModelForm
    template_name = 'admin-panel/exam/quiz/create.html'
   

    def form_valid(self, form):
        messages.success(self.request, 'ایتم ساخته شد')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('admin-panel:quiz-questions-list', kwargs={'quiz_id': self.object.id})
class QuizUpdateView(AdminPermissionRequire, UpdateView):
    """for update quiz"""

    form_class = QuizModelForm
    template_name = 'admin-panel/exam/quiz/create.html'
 
    context_object_name = 'item'
    model = Quiz


    def form_valid(self, form):
        messages.success(self.request, 'ایتم بروز رسانی شد')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('admin-panel:quiz-questions-list', kwargs={'quiz_id': self.kwargs.get('pk')})
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
    
  
    template_name = 'admin-panel/exam/questions/create-question.html'
    form_class = QuestionModelForm
    queryset = Question.objects.prefetch_related('options')


    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, pk=self.kwargs.get('quiz_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        type_of_question = form.cleaned_data.get('type_of_question')

        if type_of_question == Question.TypeOfQuestions.IMAGE_BASED and not form.cleaned_data.get('image'):
            messages.error(self.request, 'لطفا عکس را اپلود کنید')
            return self.form_invalid(form)
        elif type_of_question == Question.TypeOfQuestions.PDF_BASED and not form.cleaned_data.get('pdf_file'):
            messages.error(self.request, 'لطفا فایل pdf را وارد کنید')
            return self.form_invalid(form)
    
        form.instance.quiz = self.quiz
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['status'] = Question.TypeOfQuestions 
        data['quiz'] = self.quiz

        return data
    
    def get_success_url(self):
        messages.success(self.request, 'سوال افزوده شد')

        if self.object.type_of_question == Question.TypeOfQuestions.MULTIPLE_CHOICE  :
            messages.info(self.request, 'لطفا گزینه ها را ثبت کنید')
            return reverse_lazy('admin-panel:quiz-question-option-create', kwargs={'quiz_id': self.quiz.id, 'qid':self.object.id})
        else :
            messages.info(self.request, 'لطفا کلید پاسخ  را ثبت کنید')
            return reverse_lazy('admin-panel:quiz-question-key-create', kwargs={'quiz_id': self.quiz.id, 'qid':self.object.id})
            
 
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
class QuestionUpdateView(AdminPermissionRequire, UpdateView):
    """for create question for quiz"""
    
    queryset = Question.objects.prefetch_related('options')
    template_name = 'admin-panel/exam/questions/create-question.html'
    form_class = QuestionModelForm
    context_object_name = 'item'

    def form_valid(self, form):
        type_of_question = form.cleaned_data.get('type_of_question')
 
        if type_of_question == Question.TypeOfQuestions.IMAGE_BASED and not form.cleaned_data.get('image'):
            messages.error(self.request, 'لطفا عکس را اپلود کنید')
            return self.form_invalid(form)
        elif type_of_question == Question.TypeOfQuestions.PDF_BASED and not form.cleaned_data.get('pdf_file'):
            messages.error(self.request, 'لطفا فایل pdf را وارد کنید')
            return self.form_invalid(form)
    
        form.instance.quiz =  self.get_object().quiz 

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        self.quiz = self.get_object().quiz 

        data['status'] = Question.TypeOfQuestions 
        data['quiz'] = self.quiz 
 


        return data
    
    def get_success_url(self):
        messages.success(self.request, 'سوال بروز رسانی شد')
        self.quiz = self.get_object().quiz 


        obj = self.get_object()

        options = QuestionOption.objects.filter(question__id=obj.id)

        if self.get_object().type_of_question == Question.TypeOfQuestions.MULTIPLE_CHOICE and not options.exists():
            messages.error(self.request, 'لطفا گزینه ها را ثبت کنید')
            return reverse_lazy('admin-panel:quiz-question-option-create', kwargs={'quiz_id': self.quiz.id, 'qid':obj.id})
        
        question_key = QuestionAnswerKey.objects.filter(question__id=obj.id)

        if not question_key.exists():
            messages.error(self.request, 'لطفا کلید پاسخ  را ثبت کنید')
            return reverse_lazy('admin-panel:quiz-question-key-create', kwargs={'quiz_id': self.quiz.id, 'qid':obj.id})
        
        return reverse_lazy('admin-panel:quiz-questions-update', kwargs={**self.kwargs})

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
class QuestionDelete(AdminPermissionRequire, RedirectView):
    """for delete the questions"""
    def get_redirect_url(self, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs.get('pk')) 
        question.delete()
        messages.info(self.request, 'سوال حذف شد')
        return reverse('admin-panel:quiz-questions-list', kwargs={'quiz_id':kwargs.get('quiz_id')})
class QuestionDeleteImage(AdminPermissionRequire, RedirectView):
    """for delete the image"""

    def get_redirect_url(self, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs.get('pk')) 
        question.image = None
        question.save()
        messages.info(self.request, 'عکس حذف شد')
        
        return reverse('admin-panel:quiz-questions-update', kwargs={'quiz_id':kwargs.get('quiz_id'), 'pk':question.id})
class QuestionDeletePDF(AdminPermissionRequire, RedirectView):
    """for delete the image"""

    def get_redirect_url(self, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs.get('pk')) 
        question.pdf_file = None
        question.save()

        messages.info(self.request, 'pdf حذف شد')
        
        return reverse('admin-panel:quiz-questions-update', kwargs={'quiz_id':kwargs.get('quiz_id'), 'pk':question.id})


class QuestionAnswerKeyCreateView(AdminPermissionRequire, CreateView):
    """ for create key for question"""

    template_name = 'admin-panel/exam/key/create-key.html'
    form_class = QuestionAnwerKeyModelForm
    queryset = QuestionAnswerKey.objects.prefetch_related('question', 'question__quiz')

    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(Question, pk=kwargs.get('qid'))
        self.quiz = get_object_or_404(Quiz, pk=kwargs.get('quiz_id'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        obj = self.question
 
        options = QuestionOption.objects.filter(question__id=self.question.id)

        if obj.type_of_question == Question.TypeOfQuestions.MULTIPLE_CHOICE and not options.exists():
            messages.error(self.request, 'لطفا گزینه ها را ثبت کنید')
            return reverse_lazy('admin-panel:quiz-question-option-create', kwargs={'quiz_id': self.quiz.id, 'qid':obj.id})
 
        return reverse('admin-panel:quiz-questions-update', kwargs={'quiz_id':self.quiz.id, 'pk':self.question.id}) 

    def form_valid(self, form):
        type_of_answer = form.cleaned_data.get('type_of_answer')
 
        if type_of_answer == QuestionAnswerKey.TypeOfAnswer.IMAGE_BASED and not form.cleaned_data.get('image'):
            messages.error(self.request, 'لطفا عکس را اپلود کنید')
            return self.form_invalid(form)
        elif type_of_answer == QuestionAnswerKey.TypeOfAnswer.PDF_BASED and not form.cleaned_data.get('pdf_file'):
            messages.error(self.request, 'لطفا فایل pdf را وارد کنید')
            return self.form_invalid(form)
    
        form.instance.question =  self.question 

        messages.success(self.request, 'کلید افزوده شد')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['item']=self.question
        data['quiz']=self.quiz

        return data
class QuestionAnswerKeyUpdateView(AdminPermissionRequire, UpdateView):
    """for update the key of the question"""


    template_name = 'admin-panel/exam/key/create-key.html'
    form_class = QuestionAnwerKeyModelForm
    queryset = QuestionAnswerKey.objects.prefetch_related('question', 'question__quiz')
   
 
    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(Question, pk=kwargs.get('qid'))
        self.quiz = get_object_or_404(Quiz, pk=kwargs.get('quiz_id'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self):
        return QuestionAnswerKey.objects.get_or_create(question = self.question)[0]
    
    def get_success_url(self):
        obj = self.question
 
        options = QuestionOption.objects.filter(question__id=self.question.id)

        if obj.type_of_question == Question.TypeOfQuestions.MULTIPLE_CHOICE and not options.exists():
            messages.error(self.request, 'لطفا گزینه ها را ثبت کنید')
            return reverse_lazy('admin-panel:quiz-question-option-create', kwargs={'quiz_id': self.quiz.id, 'qid':obj.id})
 
        return reverse('admin-panel:quiz-questions-update', kwargs={'quiz_id':self.quiz.id, 'pk':self.question.id}) 

    def form_valid(self, form):
        type_of_answer = form.cleaned_data.get('type_of_answer')
 
        if type_of_answer == QuestionAnswerKey.TypeOfAnswer.IMAGE_BASED and not form.cleaned_data.get('image'):
            messages.error(self.request, 'لطفا عکس را اپلود کنید')
            return self.form_invalid(form)
        elif type_of_answer == QuestionAnswerKey.TypeOfAnswer.PDF_BASED and not form.cleaned_data.get('pdf_file'):
            messages.error(self.request, 'لطفا فایل pdf را وارد کنید')
            return self.form_invalid(form)
    
        form.instance.question =  self.question 

        messages.success(self.request, 'کلید بروز رسانی شد')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['item']=self.question
        data['quiz']=self.quiz
        data['key']=self.get_object()

        return data
class QuestionKeyDeleteImage(AdminPermissionRequire, RedirectView):
    """for delete the image"""

    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(QuestionAnswerKey, pk=kwargs.get('pk')) 
        item.image = None
        item.save()

        messages.info(self.request, 'عکس حذف شد')
        
        return reverse('admin-panel:quiz-question-key-update', kwargs={'quiz_id':kwargs.get('quiz_id'), 'qid':item.question.id})
class QuestionKeyDeletePDF(AdminPermissionRequire, RedirectView):
    """for delete the image"""

    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(QuestionAnswerKey, pk=kwargs.get('pk')) 
        item.pdf_file = None
        item.save()

        messages.info(self.request, 'pdf حذف شد')
        
        return reverse('admin-panel:quiz-question-key-update', kwargs={'quiz_id':kwargs.get('quiz_id'), 'qid':item.question.id})


class QuestionOptionsCreateView(AdminPermissionRequire, CreateView):
    """for create option to question"""

    form_class = QuestionOptionsModelForm
    template_name = 'admin-panel/exam/options/create-options.html'
    queryset = QuestionOption.objects.prefetch_related('question', 'question__quiz')

    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(Question, pk=kwargs.get('qid'))
        self.quiz = get_object_or_404(Quiz, pk=kwargs.get('quiz_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'گزینه ایجاد شد')    
        form.instance.question = self.question
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['item']=self.question
        data['quiz']=self.quiz
        return data
    
    def get_success_url(self):

        if '_add' in self.request.POST:
            return reverse('admin-panel:quiz-question-option-create', kwargs={'quiz_id':self.quiz.id, 'qid':self.question.id}) 

        obj = self.question
        question_key = QuestionAnswerKey.objects.filter(question__id=obj.id)
        if not question_key.exists():
            messages.error(self.request, 'لطفا کلید پاسخ  را ثبت کنید')
            return reverse_lazy('admin-panel:quiz-question-key-create', kwargs={'quiz_id': self.quiz.id, 'qid':obj.id})
 
        return reverse('admin-panel:quiz-questions-update', kwargs={'quiz_id':self.quiz.id, 'pk':self.question.id}) 
class QuestionOptionsUpdateView(AdminPermissionRequire, UpdateView):
    """for update option to question"""

    form_class = QuestionOptionsModelForm
    template_name = 'admin-panel/exam/options/create-options.html'
    queryset = QuestionOption.objects.prefetch_related('question', 'question__quiz')

    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(Question, pk=kwargs.get('qid'))
        self.quiz = get_object_or_404(Quiz, pk=kwargs.get('quiz_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'گزینه بروز رسانی شد')    
        form.instance.question = self.question
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['item']=self.question
        data['quiz']=self.quiz
        return data
    
    def get_success_url(self):

        if '_add' in self.request.POST:
            return reverse('admin-panel:quiz-question-option-create', kwargs={'quiz_id':self.quiz.id, 'qid':self.question.id}) 

        obj = self.question
        question_key = QuestionAnswerKey.objects.filter(question__id=obj.id)
        if not question_key.exists():
            messages.error(self.request, 'لطفا کلید پاسخ  را ثبت کنید')
            return reverse_lazy('admin-panel:quiz-question-key-create', kwargs={'quiz_id': self.quiz.id, 'qid':obj.id})
 
        return reverse('admin-panel:quiz-questions-update', kwargs={'quiz_id':self.quiz.id, 'pk':self.question.id}) 
class QuestionOptionDelete(AdminPermissionRequire, RedirectView):
    """for delete the item"""
    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(QuestionOption, pk=kwargs.get('pk')) 
        item.delete()
        messages.info(self.request, 'گزینه حذف شد')
        return reverse('admin-panel:quiz-questions-update', kwargs={'quiz_id':kwargs.get('quiz_id'), 'pk':kwargs.get('qid')})


class QuestionAnswerListView(AdminPermissionRequire, ListView):
    """for list the student anwers """
    
    template_name = 'admin-panel/exam/answers/list.html'
    context_object_name = 'items'

    def dispatch(self, request, *args, **kwargs):
      
        self.quiz = get_object_or_404(Quiz, pk=self.kwargs.get('quiz_id'))
        self.question = get_object_or_404(Question, pk=self.kwargs.get('qid'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs)  :
        context = super().get_context_data(**kwargs)
        context["quiz"] = self.quiz 
        context["question"] = self.question 
        return context

    def get_queryset(self):
        return StudentAnswer.objects.filter(quiz=self.quiz, question=self.question
        ).prefetch_related('student', 'corrected_by').all()
class QuestionAnswerCreateView(AdminPermissionRequire, CreateView):
    """ for add the answer of user"""

    template_name = 'admin-panel/exam/answers/create.html'
    context_object_name = 'item'
    form_class = StudentAnswerModelForm
 
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['selected_option'] = QuestionOption.objects.filter(question__id=self.kwargs.get('qid'))
        return kwargs
 
    
    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(Question.objects.prefetch_related('quiz', 'quiz__student'), pk=kwargs.get('qid'))
 
        self.quiz = self.question.quiz

        self.users = self.quiz.student.filter(
            answers__type_of_answer=StudentAnswer.TypeOfAnswer.NOT_ANSWERD,
            answers__question=self.question
        ).order_by('-pk').distinct().all() 

        if not self.users.exists():
            messages.success(self.request, 'کارنامه ها ی تمامی دانش اموزان این ازمون برای این سوال وارد شدند')
            return redirect(reverse('admin-panel:quiz-questions-list', kwargs={'quiz_id':self.quiz.id}))   

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs)  :
        context = super().get_context_data(**kwargs)
        context["quiz"] = self.quiz 
        context["question"] = self.question  
        context['users'] = self.users.all()

        return context

    def form_valid(self, form):
        # ذخیره اولیه فرم
        self.object = form.save(commit=False)
        
        # تنظیم student
        try:
            user_id = self.request.POST.get('user')
            
            if user_id:
                self.object.student = User.objects.get(pk=user_id)
            else:
                messages.error(self.request, 'کاربر معتبر نیست')
                return self.form_invalid(form)
            
        except (ValueError, User.DoesNotExist):
            messages.error(self.request, 'کاربر معتبر نیست')
            return self.form_invalid(form)
        
        # تنظیم quiz و question
        self.object.quiz = self.quiz
        self.object.question = self.question
        
        # تعیین نوع پاسخ
        if self.object.type_of_answer == StudentAnswer.TypeOfAnswer.NOT_ANSWERD:
            if self.object.image:
                type_of_answer = StudentAnswer.TypeOfAnswer.IMAGE_BASED
            elif self.object.pdf_file:
                type_of_answer = StudentAnswer.TypeOfAnswer.PDF_BASED
            elif self.object.selected_option:
                type_of_answer = StudentAnswer.TypeOfAnswer.OPTION
            elif self.object.is_skipped:
                type_of_answer = StudentAnswer.TypeOfAnswer.SKIPPED
            else  :
                type_of_answer = StudentAnswer.TypeOfAnswer.TEXT_BASED
        
        # استفاده از update_or_create برای جلوگیری از duplicate
        obj, created = StudentAnswer.objects.update_or_create(
            student=self.object.student,
            quiz=self.object.quiz,
            question=self.object.question,
            defaults={
                'description': self.object.description,
                'selected_option': self.object.selected_option,
                'image': self.object.image,
                'pdf_file': self.object.pdf_file,
                'is_skipped': self.object.is_skipped,
                'type_of_answer': type_of_answer,
            }
        )
        
        self.object = obj
        messages.success(self.request, 'تغییرات اعمال شد')
        return redirect(self.get_success_url())

    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
        
    def get_success_url(self):
        if 'add' in self.request.POST:
            return reverse('admin-panel:quiz-question-answer-create', kwargs={'quiz_id':self.quiz.id, 'qid':self.question.id})

        return reverse('admin-panel:quiz-question-answer-list', kwargs={'quiz_id':self.quiz.id, 'qid':self.question.id})   
class QuestionAnswerUpdateView(AdminPermissionRequire, UpdateView):
    """ for update the answer """

    template_name = 'admin-panel/exam/answers/create.html'
    context_object_name = 'item'
    form_class = StudentAnswerModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['selected_option'] = QuestionOption.objects.filter(question__id=self.kwargs.get('qid'))
        return kwargs
    
    def dispatch(self, request, *args, **kwargs):
        self.item = get_object_or_404(
            StudentAnswer.objects.prefetch_related('quiz', 'student', 'question'), 
            quiz__id=self.kwargs.get('quiz_id'), 
            question=self.kwargs.get('qid'), 
            pk=self.kwargs.get('pk')
        )
        self.quiz = self.item.quiz
        self.question = self.item.question
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs)  :
        context = super().get_context_data(**kwargs)
        context["quiz"] = self.quiz 
        context["question"] = self.question 
        return context

    def get_object(self):
        return self.item
    
    def form_valid(self, form):
        messages.success(self.request, 'تغییرات اعمال شد')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
        
    def get_success_url(self):
        if 'add' in self.request.POST:
            return reverse('admin-panel:quiz-question-answer-create', kwargs={'quiz_id':self.quiz.id, 'qid':self.question.id})

        return reverse('admin-panel:quiz-question-answer-list', kwargs={'quiz_id':self.quiz.id, 'qid':self.question.id})

