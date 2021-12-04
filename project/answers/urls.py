from django.urls import path, include
#from django.contrib.auth.views import LogoutView
from .views import IndexView, AnswerCreateView, AnswerDeleteView, AnswerUpdateView
#from .views_login import LoginView

urlpatterns = [
    path('', IndexView.as_view()),
    path('create/', AnswerCreateView.as_view(), name='answer_create'),
    path('delete/<int:pk>', AnswerDeleteView.as_view(), name='answer_delete'),
    path('update/<int:pk>', AnswerUpdateView.as_view(), name='answer_update'),
]

