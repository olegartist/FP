from datetime import datetime
from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from surveys.models import Surveys


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_count'] = str(User.objects.all().count())
        context['survey_count'] = str(Surveys.objects.all().count())

        # context['time_now'] = str(datetime.utcnow()).split(" ")[0]
        # context['last_login'] = request.

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if request.user.is_staff:
            context['type_user'] = 'Администратор'
        else:
            context['type_user'] = 'Пользователь'
        # self.object_list = self.get_queryset()
        return self.render_to_response(context)

        # if request.user.is_staff:
        #     self.template_name = 'survey/survey_admin.html'
        #     return self.render_to_response(context)
        # else:
        #     self.template_name = 'survey/survey_user.html'
        #     return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('/surveys/')
        else:
            return redirect('/users/')
