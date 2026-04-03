from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, RedirectView, View
from django.http import Http404
from ipware import get_client_ip
from .models import  StudentAnswer, Quiz, QuizView, Question, QuestionOption, UserQuizDetail
from dashboard.models import UserFavorate
from django.db.models.aggregates import Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.timezone import now, timedelta
from .forms import QuizSearchForm, AnswerForm
import random
from django.db.models import Q
from order.models import Order, OrderDetail

# Create your views here.

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
        return  queryset.order_by('-pk').all()
    

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
                ) 
                
                data['quiz_in_order'] = order.exists()
                data['order'] = order.first()
                data['order_status'] = Order.OrderStatus

            else:
                data['quiz_in_order'] = False

            data['now'] = now()
            
 
        return data
          
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

class SetQuizDetailForUser(LoginRequiredMixin, RedirectView):
    """for set quiz detail for users """

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.get('pk')
        user = self.request.user

        quiz = get_object_or_404(Quiz, pk=pk)

        if not quiz.student.filter(pk=self.request.user.id).exists() or quiz.student.filter(pk=self.request.user.id).count() != 1:
            messages.error(
                self.request, 'شما در این ازمون ثبت نام نکردید'
            )
            return  reverse('quiz:detail', kwargs={'pk': quiz.id})

        if quiz.start_at and quiz.start_at > now():
            messages.error(
                self.request, 'ازمون هنوز شروع نشده است'
            )
            return reverse('quiz:detail', kwargs={'pk': quiz.id})

        if quiz.stop_at and quiz.stop_at < now():
            messages.error(
                self.request, 'ازمون پایان یافت'
            )
            return reverse('quiz:detail', kwargs={'pk': quiz.id})

        if quiz.last_enter and quiz.last_enter < now():
            messages.error(
                self.request, 'مدت مجاز ورود به ازمون تمام شده است'
            )
            return reverse('quiz:detail', kwargs={'pk': quiz.id})

        obj, created = UserQuizDetail.objects.get_or_create(
            quiz=quiz,
            student=user,
            
        )

        if created or obj.student_start_at is None or (obj.student_finished_at <= now() and quiz.stop_at > now() and quiz and quiz.allow_to_edit_the_question_after_the_user_finish) :
            obj.student_start_at = now()
        else: 
            obj.out_of_page += 1
        obj.save()

        for question in quiz.questions.all():
            StudentAnswer.objects.get_or_create(
                student=user,
                quiz = quiz,
                question = question
            )

        messages.success(
            self.request, 'برای شما پاسخ نامه تعریف شد'
        )

        return reverse('quiz:quiz-start', kwargs={'pk': quiz.id})


class QuizStarted(LoginRequiredMixin, View):
    """
    Quiz start view - handles displaying questions to students
    """
    
    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk')
        self.request = request
        
        # Get quiz with optimized queries
        self.quiz = get_object_or_404(
            Quiz.objects.select_related('grade', 'major', 'lession'),
            id=self.pk
        )
        
        # Check if quiz detail exists for this student
        self.quiz_detail = self.quiz.detail.filter(student=request.user).first()
        if not self.quiz_detail :
            return redirect(reverse('quiz:set-details', kwargs={'pk': self.quiz.id}))
        
        # Get unsolved questions (not answered yet)
        self.unsolved_question_ids = list(
            self.quiz.questions.filter(
                student_answers__student=request.user,
 
                student_answers__type_of_answer=StudentAnswer.TypeOfAnswer.NOT_ANSWERD
            ).values_list('id', flat=True)
        )
        
        # Check if all questions are answered
        if not self.unsolved_question_ids and not self.quiz.allow_to_edit_the_answered_questions:
            messages.success(
                request, 
                'شما با موفقیت به همه سوالات پاسخ دادید و طراح این آزمون اجازه ویرایش سوالات پاسخ داده شده را نداده است'
            )
            return redirect(reverse('quiz:quiz-finished', kwargs={'pk': self.pk}))
        
        # Determine which questions to show
        if self.quiz.allow_to_edit_the_answered_questions:
            self.questions = self.quiz.questions.all()
        else:
            self.questions = self.quiz.questions.filter(
                student_answers__type_of_answer=StudentAnswer.TypeOfAnswer.NOT_ANSWERD,
                student_answers__student=request.user
            )
        
        # Handle question_id from URL (if returning to a specific question)
        question_id = kwargs.get('question_id')
        if question_id and self.quiz.allow_return_to_questions:
            try:
                self.question = self.questions.get(pk=question_id)
            except self.questions.model.DoesNotExist:
                raise Http404("سوال یافت نشد")
        else:
            # Select question based on quiz settings
            if not self.quiz.change_the_order:
                # Return first unsolved question (ordered)
                self.question = self.questions.filter(
                    student_answers__type_of_answer=StudentAnswer.TypeOfAnswer.NOT_ANSWERD
                ).first()
            else:
                # Return random unsolved question
                import random
                try:
                    self.question = self.quiz.questions.filter(
                        id__in=self.unsolved_question_ids 
                    ).get(pk=random.choice(self.unsolved_question_ids))
                except:
                    if self.quiz.allow_to_edit_the_answered_questions :
                        self.question = self.quiz.questions.first()
                    else:
                        messages.success(request, 
                            'شما با موفقیت به همه سوالات پاسخ دادید و طراح این آزمون اجازه ویرایش سوالات پاسخ داده شده را نداده است'
                        )
                        return redirect(reverse('quiz:quiz-finished', kwargs={'pk': self.pk}))

        
        # Get or create student answer
        self.student_answers, created = StudentAnswer.objects.get_or_create(
            student=request.user,
            quiz=self.quiz,
            question=self.question,
            defaults={'type_of_answer': StudentAnswer.TypeOfAnswer.NOT_ANSWERD}
        )
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        # Get solved questions (answered but not skipped)
        solved_question_ids = list(
            self.quiz.questions.filter(
                student_answers__student=request.user,
 
            ).exclude(
                student_answers__type_of_answer=StudentAnswer.TypeOfAnswer.NOT_ANSWERD
            ).values_list('id', flat=True)
        )
        
        # Get skipped questions
        skipped_question_ids = list(
            self.quiz.questions.filter(
                student_answers__student=request.user,

                student_answers__type_of_answer=StudentAnswer.TypeOfAnswer.SKIPPED
            ).values_list('id', flat=True)
        )
        
        # All questions
        all_question_ids = list(
            self.quiz.questions.values_list('id', flat=True)
        )
        remaining_seconds = ((self.quiz_detail.student_start_at + timedelta(minutes=self.quiz.time_minutes)) - now()).total_seconds()

        context = {
            'quiz': self.quiz,
            'answer': self.student_answers,
            'question': self.question,
            'solved_question': solved_question_ids,
            'solved_question_count': len(solved_question_ids),
            'skipped_question': skipped_question_ids,
            'skipped_question_count': len(skipped_question_ids),
            'unsolved_question': self.unsolved_question_ids,
            'unsolved_question_count': len(self.unsolved_question_ids),
            'all_question': all_question_ids,
            'all_question_count': len(all_question_ids),
            'quiz_detail': self.quiz_detail,
            'solved_skipped_questions': len(solved_question_ids) + len(skipped_question_ids),
            'remaining_time': max(0, int(remaining_seconds / 60)),
            'status': StudentAnswer.TypeOfAnswer,
        }

 
        return render(request, 'main/exam/start-exam.html', context)

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
        answer.save()

        messages.warning(self.request, 'سوال به حالت رد شده تبدیل شد')

        return reverse('quiz:quiz-start', kwargs={'pk':quiz_id})

class QuizFinished(LoginRequiredMixin, RedirectView):
        """quiz finished"""

        def get_redirect_url(self, *args, **kwargs):

            pk = kwargs.get('pk')
            quiz = get_object_or_404(Quiz, pk=pk, student=self.request.user)
            
            quiz_detail = UserQuizDetail.objects.get(
                quiz = quiz, 
                student = self.request.user,
            )

            quiz_detail.student_finished_at = now()
            quiz_detail.save()



            messages.success(self.request, 'از ازمون با موفقیت خارج شدید')
            messages.warning(self.request, 'خسته نباشید')

            return reverse('quiz:detail', kwargs={'pk':pk}) 

class QuizSetAnswerTextOrFiles(LoginRequiredMixin, RedirectView):
    """for upload files"""
    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(
            StudentAnswer, 
            question_id=kwargs.get('question_id'),
            quiz_id=kwargs.get('pk'),
            student=self.request.user
        )

        form = AnswerForm(self.request.POST, self.request.FILES)

        if not item.quiz.allow_to_edit_the_answered_questions:
            messages.error(self.request, 'در این ازمون اجازه تغییر پاسخ ثبت شده')
            return reverse('quiz:quiz-start', kwargs={'pk':kwargs.get('pk')})

        if form.is_valid():
            
            if text:= form.cleaned_data.get('answer'):


                item.description = text
                item.type_of_answer = StudentAnswer.TypeOfAnswer.TEXT_BASED
                
        
            if file:= form.cleaned_data.get('file'):
 
                if  file.content_type in ['application/pdf']:
                    
                    item.pdf_file = form.files.get('file') 
                    item.type_of_answer = StudentAnswer.TypeOfAnswer.PDF_BASED
                    

                else:
                    item.image = form.files.get('file')
                    item.type_of_answer = StudentAnswer.TypeOfAnswer.IMAGE_BASED
                    

            if image:= form.cleaned_data.get('image'):
                item.image = form.files.get('image')
                item.type_of_answer = StudentAnswer.TypeOfAnswer.IMAGE_BASED

            item.created_at = now() 
            item.save()
            messages.success(self.request, 'پاسخ ثبت شد')
        else:
            messages.error(self.request, form.errors)

        

        return reverse('quiz:quiz-start', kwargs={'pk':kwargs.get('pk')})

class QuizAnswerRemoveImage(LoginRequiredMixin, RedirectView):
    """for delete the image"""
    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(
            StudentAnswer, 
            question_id=kwargs.get('question_id'),
            quiz_id=kwargs.get('pk'),
            student=self.request.user
        )

        item.image = None
        item.save()
        messages.success(self.request, 'عکس حذف شد')

        

        return reverse('quiz:quiz-start', kwargs={'pk':kwargs.get('pk')})
class QuizAnswerRemovePDF(LoginRequiredMixin, RedirectView):
    """for delete the image"""
    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(
            StudentAnswer, 
            question_id=kwargs.get('question_id'),
            quiz_id=kwargs.get('pk'),
            student=self.request.user
        )

        item.pdf_file = None
        item.save()
        messages.success(self.request, 'pdf حذف شد')

        

        return reverse('quiz:quiz-start', kwargs={'pk':kwargs.get('pk')})









