from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Surveys(models.Model):
    #theme = models.CharField(max_length=255, null=False)
    theme = models.TextField(null=False)
    description = models.TextField(null=False)
    startdate = models.DateTimeField(null=False)
    enddate = models.DateTimeField(null=False)
    created = models.DateTimeField(auto_now_add=True)

    def questions(self):
        res = Questions.objects.filter(survey_id=self.id).count()
        return res

        # def __str__(self):
    #     return f'{self.theme} {self.description} {datetime.strptime(self.startdate, "%Y-%m-%d")} {datetime.strptime(self.enddate, "%Y-%m-%d")} {datetime.strptime(self.created, "%Y-%m-%d")}'

class Questions(models.Model):
    text = '0'
    one = '1'
    many = '2'
    QUEST_TYPE = [
        (text, 'Текст'),
        (one, 'Единичный'),
        (many, 'Множественный'),
    ]
    survey = models.ForeignKey(Surveys, related_name='surveys', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=False)
    type = models.CharField(max_length=1, choices=QUEST_TYPE, default=one)

    # def __str__(self):
    #     return self.QUEST_TYPE[self.type]

class Answers(models.Model):
    question = models.ForeignKey(Questions, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=False)

class Answer_Text(models.Model):
    question = models.ForeignKey(Questions, related_name='question_text', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_text', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=False)

class Answer_Daw(models.Model):
    option = models.ForeignKey(Answers, related_name='answer_daw', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_daw', on_delete=models.CASCADE)
    true = models.BooleanField(default=False)

class Answered(models.Model):
    survey = models.ForeignKey(Surveys, related_name='survey_answer', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_answer', on_delete=models.CASCADE)


# class User_Answer_Text(models.Model):
#     user = models.ForeignKey(User, related_name='user_text', on_delete=models.CASCADE)
#     answer = models.ForeignKey(Answer_Text, related_name='answer_text', on_delete=models.CASCADE)
#     text = models.CharField(max_length=255)
#
# class User_Answer_Daw(models.Model):
#     user = models.ForeignKey(User, related_name='user_daw', on_delete=models.CASCADE)
#     answer = models.ForeignKey(Answer_Daw, related_name='answer_daw', on_delete=models.CASCADE)
#     true = models.BooleanField(default=False)
