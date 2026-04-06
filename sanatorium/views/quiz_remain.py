from django.views.generic import ListView, View
from quiz.models import Quiz, StudentAnswer, Question, QuestionAnswerKey
from sanatorium.mixins import SanatorPermissionRequire
from django.db.models import Q
from django.db.models.aggregates import Count
from django.shortcuts import render, redirect
from sanatorium.forms import SanatoriumCorecctingPanelForm
from django.http import Http404
from django.contrib import messages
from django.utils.timezone import now
from django.db.transaction import atomic
from django.urls import reverse
from sanatorium.models import SanatoriumWallet, WalletDetails

class SanatoriumPendingExamList(SanatorPermissionRequire, ListView):
    template_name =  'sanatorium/quiz-remain/08-pending-exams.html'
    context_object_name = 'items'
    paginate_by = 50

    def get_queryset(cls):
        cls.queryset = Quiz.objects.filter(sanatorium=cls.request.user, is_active=True).prefetch_related('grade', 'major', 'lession', 'student').annotate(
            question_count=Count('questions'),
        ).order_by('-pk')
        return cls.queryset

    def get_context_data(cls, **kwargs):
        data = super().get_context_data(**kwargs)

        data['status'] = Quiz.QuizStatus
        data['corrected'] = cls.queryset.filter(
            Q(status=Quiz.QuizStatus.CORRECTED) |
            Q(status=Quiz.QuizStatus.RESULTS_PUBLISHED) 
        ).count()
        data['wait_corrected'] = cls.queryset.filter(
            Q(status=Quiz.QuizStatus.FINISHED) |
            Q(status=Quiz.QuizStatus.WAITING_CORRECTION) 
        ).count()


        return data
 

class SanatoriumReportsListPerStudentOfExam(SanatorPermissionRequire, ListView):
    """for list the reposrts"""
    template_name =  'sanatorium/quiz-remain/10-exam-questions.html'
    context_object_name = 'items'
    paginate_by = 50
    
    def get_queryset(self):
        self.pk = self.kwargs.get('pk')
        self.query = StudentAnswer.objects.filter(
            quiz__id=self.pk,
            quiz__sanatorium=self.request.user, 
            quiz__is_active=True
        )
        

        self.query = self.query.prefetch_related('question', 'quiz__grade', 'quiz__major', 'quiz__lession', 'quiz').order_by('-pk')

 
        return self.query
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        queryset =  self.get_queryset()
        data['corrected'] = queryset.filter(corrected_at__isnull=False, corrected_by=self.request.user).count()
        data['not_corrected'] = queryset.filter(corrected_at__isnull=True, corrected_by__isnull=True).count()
 
        data['all_corrected'] = queryset.count()
        data['correction_type'] = StudentAnswer.TypeOfCorrect
        try:
            data['corrected_percent'] = 100*(int(data['corrected']) / int(data['all_corrected']))
        except:
            data['corrected_percent'] = 0

        data['quiz'] = Quiz.objects.filter(pk=self.pk, sanatorium=self.request.user).first()
        return data


class SanatoriumQuestionDetailPerStudentOfExam(SanatorPermissionRequire, View):
    """for correcting the student answear"""
    
    template_name =  'sanatorium/quiz-remain/11-question-detail.html'
    
    def get_queryset(cls):

        cls.pk = cls.kwargs.get('pk')

        cls.report_id = cls.kwargs.get('report_id')


        answer = StudentAnswer.objects.filter(
            quiz__allow_to_edit_anwerd_by_sanatorium=True,
            quiz__pk=cls.pk,
            quiz__sanatorium=cls.request.user, 
        ).prefetch_related('question','question__options' , 
            'student', 'quiz', 'selected_option', 
            'quiz__major', 'quiz__grade', 'quiz__lession'
        )
 
        if cls.report_id:
            answer = answer.filter(pk=cls.report_id)
            return answer.first()

        else:
            answer = answer.filter(
            corrected=StudentAnswer.TypeOfCorrect.not_corrected,
            corrected_at__isnull=True,
            corrected_by__isnull=True,
            )
            
            return answer.order_by('question__pk').first()
    
    def get(cls, request, *args, **kwargs):

        queryset = cls.get_queryset()

        if not queryset :
            messages.success(request, 'از پاسخ های شما متشکریم')
            if queryset is None:
                quiz = Quiz.objects.filter(pk=kwargs.get('pk'), sanatorium=request.user)
                if quiz.exists() and quiz.count() == 1:
                    quiz = quiz.first()
                    quiz.status = Quiz.QuizStatus.CORRECTED
                    quiz.save()
                    messages.success(request, 'ازمون به حالت تصحیح شده تغییر یافت')


            return redirect(reverse('sanatorium:exam-student-question-list', kwargs={'pk':kwargs.get('pk')}))



        inital = {
            'satantorium_message': request.POST.get('satantorium_message') or queryset.satantorium_message if queryset.satantorium_message else  None,
            'score': request.POST.get('score') or queryset.score if queryset.score else None,
            'corrected': request.POST.get('corrected')  or queryset.corrected if queryset.corrected else None,
        }

        context = {
            'item': queryset,
            'form': SanatoriumCorecctingPanelForm(initial=inital),
            'type_of_questions': Question.TypeOfQuestions,
            'type_of_key': QuestionAnswerKey.TypeOfAnswer,
            'type_of_answer': StudentAnswer.TypeOfAnswer
        }

        return render(request, cls.template_name, context)

    def post(cls, request, *args, **kwargs):
        form = SanatoriumCorecctingPanelForm(request.POST or None)

        if form.is_valid():
            
            try:
                with atomic():
                    queryset = cls.get_queryset()
               
                    queryset.corrected_by = request.user
                    queryset.corrected_at = now()
                    queryset.corrected = form.cleaned_data.get('corrected')
                    queryset.satantorium_message = form.cleaned_data.get('satantorium_message') or 'پیام از طرف مصحح ارسال نشده است'

                    score = float(form.cleaned_data.get('score')) 
                    if score <= 0:
                        queryset.score = 0
                    elif score >= queryset.question.score:
                        queryset.score = queryset.question.score
                    else :
                        queryset.score = score
                    
                    queryset.save()
                
                    messages.success(request, 'نمره ثبت شد')

                    wallet = SanatoriumWallet.objects.get_or_create(
                        user=request.user, quiz=queryset.quiz
                    )[0]

                    wallet_detail = WalletDetails.objects.get_or_create(
                        wallet=wallet, answer=queryset
                    )[0]
                    messages.warning(request, 'مبلغ {} تومان به کیف پول شما اضافه شد '.format(wallet_detail.get_item_price()))

                    
                return redirect(reverse('sanatorium:exam-student-question-detail', kwargs={'pk':kwargs.get('pk')}))

            
            except Exception as E:
                print(cls.__class__.__name__, E)
                messages.error(request, 'در ارسال داده های نمره خطا رخ داده است لطفا در پارامتر های ورودی دقت فرمایید')
                return cls.get(request, *args, **kwargs)


        else:
            messages.error(request, form.errors)
            return cls.get(request, *args, **kwargs)
