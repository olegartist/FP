from datetime import datetime
from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from surveys.models import Surveys, Questions, Answers


class IndexView(LoginRequiredMixin, ListView):
    model = Surveys
    template_name = 'users/list_surveys.html'
    context_object_name = 'surveys'
    object_list = None

    def get(self, request, *args, **kwargs):
        #if request.user.is_staff: return redirect('/')
        context = self.get_context_data()
        time_now = datetime.utcnow()
        context['time_now'] = time_now  # добавим переменную текущей даты time_now
        context['surveys_count'] = Surveys.objects.all().count()
        context['surveys'] = Surveys.objects.filter(enddate__date__gte=time_now).order_by('-id')
        self.object_list = self.get_queryset()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        sr = str(self.kwargs.get('sr'))
        return redirect('/users/questions/'+sr)

class QuestionView(LoginRequiredMixin, ListView):
    model = Questions
    template_name = 'users/list_questions.html'
    context_object_name = 'questions'
    object_list = None

    def get(self, request, *args, **kwargs):
        #if request.user.is_staff: return redirect('/')
        sr = str(self.kwargs.get('sr'))
        context = self.get_context_data()
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['theme'] = Surveys.objects.get(pk=sr).theme
        context['description'] = Surveys.objects.get(pk=sr).description
        context['questions_count'] = Questions.objects.filter(survey=sr).count()
        context['questions'] = Questions.objects.filter(survey=sr).order_by('-id')
        context['sr'] = sr
        context['nn'] = 0
        # self.object_list = self.get_queryset()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # id = self.kwargs.get('sr')
        return redirect('/users/')
