from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import QuestionAnswerKey, QuestionBank, QuestionOption, QuestionLessonCategory, QuestionPossible, QuestionView
from django.http import Http404
from ipware import get_client_ip
from django.db.models.aggregates import Count 


# Create your views here.


class QuestionsView(ListView):
    """
    for listing the questions
    """

    template_name = 'main/question-bank/list.html'
    context_object_name = 'items'
    paginate_by = 50

    def get_queryset(self):
        queryset = QuestionBank.objects.filter(is_active=True).prefetch_related('possible', 'category', 'options', 'answer_key')

        queryset = queryset.annotate(views_counts=Count('views'))

        pk = self.kwargs.get('pk')
        category_id = self.kwargs.get('category_id')

        if pk:
            queryset = queryset.filter(id=pk)

            try:
                ip, is_rout = get_client_ip(self.request)
                view = QuestionView.objects.get_or_create(ip=ip, blog_id=pk)

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

                    
        if category_id:
            queryset.filter(category__id=category_id)

        return  queryset.all()
    

    def get_template_names(self):
        pk = self.kwargs.get('pk')

        if pk :
            return 'main/question-bank/detail.html'
       
        return self.template_name
    
    def get_context_object_name(self, object_list):
        pk = self.kwargs.get('pk')

        if pk :
            return 'item'
       
        return self.context_object_name 
    
    def get_paginate_by(self, queryset):

        pk = self.kwargs.get('pk')

        if pk :
            return None

        return self.paginate_by

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')

        if not pk :
            data['possible'] = QuestionPossible.objects.filter(is_active=True).all() 
            data['categories'] = QuestionLessonCategory.objects.filter(is_active=True).all() 
            data['questions_type'] = QuestionBank.TypeOfQuestions.choices

        return data
 

