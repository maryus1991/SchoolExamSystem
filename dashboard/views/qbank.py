from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages



class QuestionList(TemplateView):
    template_name = 'dashboard/qbank/09-question-list.html'

class QuestionDetail(TemplateView):
    template_name = 'dashboard/qbank/10-question-detail.html'
