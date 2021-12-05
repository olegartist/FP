from datetime import datetime
from django.shortcuts import render, reverse, redirect, HttpResponse
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from surveys.models import Surveys, Questions

class IndexView(LoginRequiredMixin, ListView):
    model = Questions
    template_name = 'questions/list_admin.html'
    context_object_name = 'questions'
    object_list = None

    def get(self, request, *args, **kwargs):
        sr = str(self.kwargs.get('sr'))
        context = self.get_context_data()
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['theme'] = Surveys.objects.get(pk=sr).theme
        context['questions_count'] = Questions.objects.filter(survey=sr).count()
        context['questions'] = Questions.objects.filter(survey=sr).order_by('-id')
        context['sr'] = sr
        # self.object_list = self.get_queryset()
        if not request.user.is_staff:
            return redirect('/')
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # id = self.kwargs.get('sr')
        return redirect('/surveys/')


class QuestionCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'questions/create.html'

    def get(self, request, *args, **kwargs):
        # sr = str(self.kwargs.get('sr'))
        context = self.get_context_data()
        if not request.user.is_staff:
            return redirect('/')
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        sr = str(self.kwargs.get('sr'))
        if not request.POST['text']:
            return redirect('/surveys/questions/' + sr)
        question = Questions(
            survey_id=int(sr),
            text=request.POST['text'],
            type=request.POST['selected'],
        )
        question.save()
        return redirect('/surveys/questions/' + sr)


class QuestionDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'questions/delete.html'

    def get(self, request, *args, **kwargs):
        sr = str(self.kwargs.get('sr'))
        qs = str(self.kwargs.get('pk'))
        context = self.get_context_data()
        context['question'] = Questions.objects.get(pk=qs)
        context['sr'] = sr
        if not request.user.is_staff:
            return redirect('/')
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        sr = str(self.kwargs.get('sr'))
        qs = str(self.kwargs.get('pk'))
        Questions.objects.filter(pk=qs).delete()
        return redirect('/surveys/questions/' + sr)


class QuestionUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'questions/update.html'

    def get(self, request, *args, **kwargs):
        sr = str(self.kwargs.get('sr'))
        qs = str(self.kwargs.get('pk'))
        context = self.get_context_data()
        context['text'] = Questions.objects.get(pk=qs).text
        context['type'] = Questions.objects.get(pk=qs).type
        context['sr'] = sr
        context['qs'] = qs
        if not request.user.is_staff:
            return redirect('/')
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        sr = str(self.kwargs.get('sr'))
        qs = str(self.kwargs.get('pk'))
        if not request.POST['text']:
            return redirect('/surveys/questions/' + sr)
        question = Questions.objects.get(pk=qs)
        question.text = request.POST['text']
        question.type = request.POST['selected']
        question.save()
        return redirect('/surveys/questions/' + sr)
