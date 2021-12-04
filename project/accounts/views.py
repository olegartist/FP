from django.shortcuts import render, reverse, redirect, HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib.auth.models import User
#from datetime import datetime

class LoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/login.html', {})

    def post(self, request, *args, **kwargs):
        #print(request.user)
        username = (request.POST.get('username'))
        password = (request.POST.get('password'))
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # юсер существут и ативный
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            if not username or username is None:
                # Anonim
                username = str(int(str(User.objects.latest('pk').id)) + 1)
                user = User.objects.create_user(username=username, password='')
                auth.login(request, user)
            else:
                if not User.objects.filter(username=username).exists():
                    # 'юсер не существут')
                    user = User.objects.create_user(username=username, password=password)
                    auth.login(request, user)
                    return HttpResponseRedirect("/")
                return HttpResponseRedirect('login_error') # юсер существут, но не верный пароль

        return redirect('/') #'logins:login'
