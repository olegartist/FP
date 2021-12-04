from datetime import datetime
from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Surveys, Questions


class IndexView(LoginRequiredMixin, ListView):
    model = Surveys
    template_name = ''
    context_object_name = 'surveys'
    object_list = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['surveys_count'] = Surveys.objects.all().count()
        context['surveys'] = Surveys.objects.all().order_by('-id')
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        self.object_list = self.get_queryset()
        if request.user.is_staff:
            self.template_name = 'surveys/list_admin.html'
            return self.render_to_response(context)
        else:
            self.template_name = 'surveys/list_user.html'
            return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return redirect('/surveys/')

class SurveyCreateView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if request.user.is_staff:
            self.template_name = 'surveys/create.html'
            return self.render_to_response(context)
        else:
            return redirect('/surveys/')

    def post(self, request, *args, **kwargs):
        if request.POST['startdate'] == '' or request.POST['enddate'] == '':
            return redirect('/surveys/')
        surveys = Surveys(
            theme=request.POST['theme'],
            description=request.POST['description'],
            startdate=datetime.strptime(request.POST['startdate'], '%Y-%m-%d'),
            enddate=datetime.strptime(request.POST['enddate'], '%Y-%m-%d'),
        )
        surveys.save()
        return redirect('/surveys/')

class SurveyDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'surveys/delete.html'
    queryset = Surveys.objects.all()
    success_url = '/surveys/'

class SurveyUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'surveys/update.html'
    success_url = '/surveys/'

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['pk'] = id
        context['theme'] = Surveys.objects.filter(pk=id)[0].theme
        context['description'] = Surveys.objects.filter(pk=id)[0].description
        context['startdate'] = str(Surveys.objects.filter(pk=id)[0].startdate).split(" ")[0]
        context['enddate'] = str(Surveys.objects.filter(pk=id)[0].enddate).split(" ")[0]
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        # self.object_list = self.get_queryset()
        if request.user.is_staff:
            self.template_name = 'surveys/update.html'
            return self.render_to_response(context)
        else:
            self.template_name = 'surveys/list_user.html'
            return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')

        if request.POST['enddate'] == '' or not request.POST['theme']:
            return redirect('/surveys/')
        surveys = Surveys.objects.get(pk=id)
        surveys.theme = request.POST['theme']
        surveys.description = request.POST['description']
        # surveys.startdate=datetime.strptime(request.POST['startdate'], '%Y-%m-%d')
        surveys.enddate = datetime.strptime(request.POST['enddate'], '%Y-%m-%d')
        surveys.save()
        return redirect('/surveys/')
