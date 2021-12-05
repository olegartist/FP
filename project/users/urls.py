from django.urls import path, include
from .views import IndexView, QuestionView#, SurveyDeleteView, SurveyUpdateView
#from .views_login import LoginView

urlpatterns = [
    path('', IndexView.as_view()),
    # path('create/', SurveyCreateView.as_view(), name='survey_create'),
    # path('update/<int:pk>/', SurveyUpdateView.as_view(), name='survey_update'),
    # path('delete/<int:pk>', SurveyDeleteView.as_view(), name='survey_delete'),
    path('questions/<int:sr>/', QuestionView.as_view(), name='user_survey'),
]

