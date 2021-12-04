from django.urls import path, include
#from django.contrib.auth.views import LogoutView
from .views import IndexView, QuestionCreateView, QuestionDeleteView, QuestionUpdateView
#from .views_login import LoginView

urlpatterns = [
    path('', IndexView.as_view()),
    path('create/', QuestionCreateView.as_view(), name='question_create'),
    path('delete/<int:pk>', QuestionDeleteView.as_view(), name='question_delete'),
    path('update/<int:pk>', QuestionUpdateView.as_view(), name='question_update'),
    path('answers/<int:qs>/', include('answers.urls')),
]

