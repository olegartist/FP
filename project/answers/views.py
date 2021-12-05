from datetime import datetime
from django.shortcuts import render, reverse, redirect, HttpResponse
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from surveys.models import Surveys, Questions, Answers


class IndexView(LoginRequiredMixin, ListView):
    model = Answers
    template_name = 'answers/list_admin.html'
    context_object_name = 'answers'
    object_list = None

    def get(self, request, *args, **kwargs):
        sr = str(self.kwargs.get('sr'))
        qs = str(self.kwargs.get('qs'))
        context = self.get_context_data()
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['theme'] = Surveys.objects.get(pk=sr).theme
        context['text'] = Questions.objects.get(pk=qs).text
        context['type'] = Questions.objects.get(pk=qs).type
        context['answers_count'] = Answers.objects.filter(question=qs).count()
        context['answers'] = Answers.objects.filter(question=qs).order_by('-id')
        context['sr'] = sr
        context['qs'] = qs
        # self.object_list = self.get_queryset()
        if not request.user.is_staff:
            return redirect('/')
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # id = self.kwargs.get('sr')
        qs = str(self.kwargs.get('qs'))
        return redirect('answers/'+qs)


class AnswerCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'answers/create.html'

    def get(self, request, *args, **kwargs):
        sr = str(self.kwargs.get('sr'))
        qs = str(self.kwargs.get('qs'))
        context = self.get_context_data()
        if not request.user.is_staff:
            return redirect('/')
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        sr = str(self.kwargs.get('sr'))
        qs = str(self.kwargs.get('qs'))
        if not request.POST['text']:
            return redirect(f'/surveys/questions/{sr}/answers/{qs}')
        answer = Answers(
            question_id=int(qs),
            text=request.POST['text'],
        )
        answer.save()
        return redirect(f'/surveys/questions/{sr}/answers/{qs}')

class AnswerDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'answers/delete.html'

    def get(self, request, *args, **kwargs):
        sr = str(self.kwargs.get('sr'))
        qs = str(self.kwargs.get('qs'))
        aw = str(self.kwargs.get('pk'))
        context = self.get_context_data()
        context['answer'] = Answers.objects.get(pk=aw)
        context['sr'] = sr
        context['qs'] = qs
        context['aw'] = aw
        if not request.user.is_staff:
            return redirect('/')
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        sr = str(self.kwargs.get('sr'))
        qs = str(self.kwargs.get('qs'))
        aw = str(self.kwargs.get('pk'))
        Answers.objects.filter(pk=aw).delete()
        return redirect(f'/surveys/questions/{sr}/answers/{qs}')

class AnswerUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'answers/update.html'

    def get(self, request, *args, **kwargs):
        sr = str(self.kwargs.get('sr'))
        qs = str(self.kwargs.get('qs'))
        aw = str(self.kwargs.get('pk'))
        context = self.get_context_data()
        context['text'] = Answers.objects.get(pk=aw).text
        context['sr'] = sr
        context['qs'] = qs
        context['aw'] = aw
        if not request.user.is_staff:
            return redirect('/')
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        sr = str(self.kwargs.get('sr'))
        qs = str(self.kwargs.get('qs'))
        aw = str(self.kwargs.get('pk'))
        if not request.POST['text']:
            return redirect(f'/surveys/questions/{sr}/answers/{qs}')
        answer = Answers.objects.get(pk=aw)
        answer.text = request.POST['text']
        answer.save()
        return redirect(f'/surveys/questions/{sr}/answers/{qs}')
