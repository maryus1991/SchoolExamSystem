from django.shortcuts import render
from django.views.generic import ListView
from django.http import Http404
from django.shortcuts import render
from ipware import get_client_ip
from .models import GradeCategories, LessionCategories, MajorCategories, Quiz, QuizView
from django.db.models.aggregates import Count
from django.contrib import messages
# Create your views here.


class QuizListDetailView(ListView):
    """
    for listing the questions
    """

    template_name_list = 'main/exam/list.html'
    template_name_detail = 'main/exam/detail.html'
    context_object_name_list = 'items'
    context_object_name_Detail = 'item'
    paginate_by = 25

    def get_queryset(self):
        queryset = Quiz.objects.filter(is_active=True
        ).prefetch_related(
            'grade', 'major', 'lession'
        )

        queryset = queryset.annotate(views_count=Count('views'), question_count=Count('questions'))

        pk = self.kwargs.get('pk')
        grade_category_id = self.kwargs.get('grade_category_id')
        lession_category_id = self.kwargs.get('lession_category_id')
        major_category_id = self.kwargs.get('major_category_id')

        if pk:
            queryset = queryset.filter(id=pk)

            try:
                ip, is_rout = get_client_ip(self.request)
                view = QuizView.objects.get_or_create(ip=ip, blog_id=pk)

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

                    
        if grade_category_id:queryset.filter(grade__id=grade_category_id)
        if lession_category_id:queryset.filter(major__id=lession_category_id)
        if major_category_id:queryset.filter(lession__id=major_category_id)

 

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
            data['grade'] = GradeCategories.objects.filter(is_active=True).all() 
            data['lession'] = LessionCategories.objects.filter(is_active=True).all() 
            data['major'] = MajorCategories.objects.filter(is_active=True).all() 
            data['status'] = Quiz.QuizStatus.choices 
 
        return data
 