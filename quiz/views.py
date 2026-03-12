from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, RedirectView, View
from django.http import Http404
from ipware import get_client_ip
from .models import  StudentAnswer, Quiz, QuizView, Question, QuestionOption
from dashboard.models import UserFavorate
from django.db.models.aggregates import Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.timezone import now
from .forms import QuizSearchForm
import random
from django.db.models import Q
from order.models import Order, OrderDetail

# Create your views here.

class QuizSetAnswerTextOrFiles(LoginRequiredMixin, RedirectView):
    pass

class QuizSetSkippedToQuestion(LoginRequiredMixin, RedirectView):
    """for skipped the question"""

    def get_redirect_url(self, *args, **kwargs):
        quiz_id = kwargs.get('pk')
        question_id= kwargs.get('question_id')  

        quiz = get_object_or_404(Quiz, pk=quiz_id, student=self.request.user)
        question = get_object_or_404(Question, quiz=quiz, pk=question_id)
        answer = StudentAnswer.objects.get_or_create(
            quiz = quiz,
            student = self.request.user,
            question = question
        )[0]
        
 
        answer.type_of_answer = StudentAnswer.TypeOfAnswer.SKIPPED
        answer.is_skipped = True 
        answer.created_at = now() 
        answer.save()

        messages.warning(self.request, 'سوال به حالت رد شده تبدیل شد')

        return reverse('quiz:quiz-start', kwargs={'pk':quiz_id})

class QuizSetAnswerOptions(LoginRequiredMixin, RedirectView):
    
    """for set the chosen option for questions"""

    def get_redirect_url(self, *args, **kwargs):
        quiz_id = kwargs.get('pk')
        option_id= kwargs.get('option_id') 
        question_id= kwargs.get('question_id')  

        quiz = get_object_or_404(Quiz, pk=quiz_id, student=self.request.user)
        question = get_object_or_404(Question, quiz=quiz, pk=question_id)
        option = get_object_or_404(QuestionOption, question=question, pk=option_id)

        if quiz.allow_to_edit_the_answered_questions:
            answer = StudentAnswer.objects.get_or_create(
                quiz = quiz,
                student = self.request.user,
                question = question
            )[0]
            
            answer.selected_option = option
            answer.type_of_answer = StudentAnswer.TypeOfAnswer.OPTION 
            answer.created_at = now() 
            answer.save()

            messages.success(self.request, 'پاسخ با موفقیت ثبت شد')
        else:
            messages.error(self.request, 'در این ازمون اجازه تغییر پاسخ ثبت شده')

        return reverse('quiz:quiz-start', kwargs={'pk':quiz_id})

class QuizFinished(LoginRequiredMixin, RedirectView):
    """quiz finished"""

    def get_redirect_url(self, *args, **kwargs):

        pk = kwargs.get('pk')
        quiz = get_object_or_404(Quiz, pk=pk, student=self.request.user)
        quiz.finished_at = now()
        quiz.save()
        for question in quiz.questions.all():
            StudentAnswer.objects.get_or_create(
                student=self.request.user,
                quiz=quiz,
                question=question
            )

        messages.success(self.request, 'از ازمون با موفقیت خارج شدید')
        messages.warning(self.request, 'خسته نباشید')

        return reverse('quiz:detail', kwargs={'pk':pk}) 

class QuizStarted(LoginRequiredMixin, View):
    """
    quiz start
    """
    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk')

        if not self.pk:
            messages.error(
            request, 'یافت نشد'
            )
            raise Http404()
        

        self.queryset = Quiz.objects.filter(id=self.pk
        ).prefetch_related('grade', 'major', 'lession', 
        'student', 'questions', 'questions__options', 
        'questions__student_answers' )
    

        if self.queryset.count() != 1 or not self.queryset.exists():
   
            messages.error(
                request, 'یافت نشد'
            )
            raise Http404()

        self.queryset = self.queryset.first()

        if not self.queryset.student.filter(pk=request.user.id).exists() or self.queryset.student.filter(pk=request.user.id).count() != 1:
            messages.error(
                request, 'شما در این ازمون ثبت نام نکردید'
            )
            return redirect(reverse('quiz:detail', kwargs={'pk': self.pk}))
        
        if self.queryset.start_at and self.queryset.start_at > now():
            messages.error(
                request, 'ازمون هنوز شروع نشده است'
            )
            return redirect(reverse('quiz:detail', kwargs={'pk': self.pk}))

        if self.queryset.stop_at and self.queryset.stop_at < now():
            messages.error(
                request, 'ازمون پایان یافت'
            )
            return redirect(reverse('quiz:detail', kwargs={'pk': self.pk}))

        '''
        شرظ بایین باید درست بشود تا برای هر سوال برای ندت زمان ورود گیر نده
        '''
        # if self.queryset.last_enter and self.queryset.last_enter < now() and not self.queryset.student_answers.filter(student=request.user).exists():
        #     messages.error(
        #         request, 'مدت مجاز ورود به ازمون تمام شده است'
        #     )
        #     return redirect(reverse('quiz:detail', kwargs={'pk': self.pk}))

        self.quiz = self.queryset

        if self.queryset.allow_to_edit_the_answered_questions:
            self.questions = self.queryset.questions
        else:
            self.questions = self.queryset.questions.filter(
                student_answers__user=request.user
            )

        self.solved_question = self.questions.filter(
            student_answers__student=request.user,
            student_answers__is_skipped=False,
            student_answers__type_of_answer__isnull=False
            ).values_list('id', flat=True)
 

        self.skipped_question = self.questions.filter(
            student_answers__student=request.user,
            student_answers__is_skipped=True,
            ).values_list('id', flat=True)


        self.unsolved_question = self.questions.filter(
            student_answers__student=request.user,
            student_answers__is_skipped=False,
            student_answers__type_of_answer__isnull=True
            ).values_list('id', flat=True)

   

        self.all_question = self.questions.values_list('id', flat=True)
        
        question_id = kwargs.get('question_id')
        if question_id and self.queryset.allow_return_to_questions  :
            self.question = self.questions.get(pk=question_id)
            self.student_answers = StudentAnswer.objects.get_or_create(
            student=request.user,
            quiz = self.quiz,
            question = self.question
            )[0]

            return super().dispatch(request, *args, **kwargs)
                
    
        if self.queryset.change_the_order and not self.queryset.allow_to_edit_the_answered_questions:

        
            self.questions = self.questions.filter(
                student_answers__student=request.user,
                student_answers__is_skipped=False,
                student_answers__type_of_answer__isnull=True
                    )
            
            if not self.questions.exists():
                messages.warning(
                    request, 'سوال بدون پاسخ ندارید و اجازه ویرایش پاسخ ها را ندارید'
                    )
                return redirect(reverse('quiz:detail', kwargs={'pk': self.pk}))

            self.unsolved_question = self.questions.values_list('id', flat=True)
            pk = random.choice(self.unsolved_question)
    
            self.question = self.questions.get(pk=pk)
            
        else:
            self.question = self.questions.filter(
                student_answers__type_of_answer__isnull=True,
                student_answers__student=request.user
            ).last()

        self.student_answers = StudentAnswer.objects.get_or_create(
            student=request.user,
            quiz = self.quiz,
            question = self.question
        )[0]

        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):
        context = {
            'quiz': self.quiz,
            'answer': self.student_answers ,
            'question': self.question, 
            'solved_question': self.solved_question, 
            'skipped_question': self.skipped_question, 
            'unsolved_question': self.unsolved_question, 
            'all_question': self.all_question, 
            'solved_skipped_questions': int(self.solved_question.count()) + int(self.skipped_question.count()), 
        }
        return render(request, 'main/exam/start-exam.html', context)
    
class AddToFavorate(LoginRequiredMixin, RedirectView):
    """for add quiz to favorate"""

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        quiz_id = kwargs.get('pk')

        try:
            user_favore_obj = UserFavorate.objects.get_or_create(
                user=user
            )[0]
            user_favore_obj.quiz.add(
                quiz_id
            )
            user_favore_obj.save()
            messages.success(
                self.request, 'اضافه شد'
            )

        except Exception as E:
            messages.error(
                self.request, 'مشکلی پیش اومده'
            )
            print(self.__class__.__name__, E)

        return reverse('quiz:detail', kwargs={'pk':quiz_id})

class RemoveToFavorate(LoginRequiredMixin, RedirectView):
    """for add quiz to favorate"""

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        quiz_id = kwargs.get('pk')

        try:
            user_favore_obj = UserFavorate.objects.get_or_create(
                user=user
            )[0]

            user_favore_obj.quiz.remove(
                quiz_id
            )
            user_favore_obj.save()
            messages.success(
                self.request, 'حذف  شد'
            )

        except Exception as E:
            messages.error(
                self.request, 'مشکلی پیش اومده'
            )
            print(self.__class__.__name__, E)

        return reverse('quiz:detail', kwargs={'pk':quiz_id})

class QuizListDetailView(ListView):
    """
    for listing the questions
    """

    template_name_list = 'main/exam/list.html'
    template_name_detail = 'main/exam/detail.html'
    context_object_name_list = 'items'
    context_object_name_Detail = 'item'
    paginate_by = 50

    def get_queryset(self):
        queryset = Quiz.objects.filter(is_active=True).prefetch_related('grade', 'major', 'lession')

        queryset = queryset.annotate(views_count=Count('views'), question_count=Count('questions'))

        pk = self.kwargs.get('pk')
        grade_category_id = self.kwargs.get('grade_category_id')
        lession_category_id = self.kwargs.get('lession_category_id')
        major_category_id = self.kwargs.get('major_category_id')

        if pk:
            queryset = queryset.filter(id=pk)

            try:
                ip, is_rout = get_client_ip(self.request)
                view = QuizView.objects.get_or_create(ip=ip, quiz_id=pk)

                if not view[1]:
                    view[0].count += 1
                    view[0].save()

                if view[0].count == 0:
                    view[0].count = 1
                    view[0].save()

            except Exception as e:
               print(self.__class__.__name__, e)   

            if not queryset.exists() and queryset.count() != 1:
                raise Http404('obj not found')
            return  queryset.first()
        
        else:
            form = QuizSearchForm(self.request.GET or None)
            if form.is_valid():
                if name := form.cleaned_data.get('name'):
                    queryset=queryset.filter(Q(name__contains=name) | Q(description__contains=name) | Q(section__contains=name) )
                if status := form.cleaned_data.get('status'):
                    if status != Quiz.QuizStatus.ALL_STATUS:
                        queryset=queryset.filter(status=status)

                if lession := form.cleaned_data.get('lession'):
                    queryset=queryset.filter(lession=lession)
                if grade := form.cleaned_data.get('grade'):
                    queryset=queryset.filter(grade=grade)
                if major := form.cleaned_data.get('major'):
                    queryset=queryset.filter(major=major)
                    

                    
        if grade_category_id:queryset=queryset.filter(grade__id=grade_category_id)
        if lession_category_id:queryset=queryset.filter(major__id=lession_category_id)
        if major_category_id:queryset=queryset.filter(lession__id=major_category_id)
        return  queryset.all()
    

    def get_template_names(self):
        pk = self.kwargs.get('pk')

        if pk :
            return self.template_name_detail
       
        return self.template_name_list
    
    def get_context_object_name(self, object_list):
        pk = self.kwargs.get('pk')

        if pk :
            return self.context_object_name_Detail
       
        return self.context_object_name_list
    
    def get_paginate_by(self, queryset):
        pk = self.kwargs.get('pk')
        if pk :
            return None
        if self.get_queryset() :
            return self.paginate_by
        
        messages.warning(
            self.request, 'موردی یافت نشد'
        )
        return None
    

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')

        if not pk :
            data['form'] = QuizSearchForm(self.request.GET or None)
        else :
            if self.request.user.is_authenticated:

                order = OrderDetail.objects.filter(
                    order__user=self.request.user, 
                    quiz__pk=pk,
                ).filter(
                    Q(order__status=Order.OrderStatus.active) | Q(order__status=Order.OrderStatus.paid)  
                )
                
                data['quiz_in_order'] = order.exists()
                data['order'] = order.first()
                data['order_status'] = Order.OrderStatus

            else:
                data['quiz_in_order'] = False

            data['now'] = now()
            
 
        return data
 