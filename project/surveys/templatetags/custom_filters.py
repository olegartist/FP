from django import template
from surveys.models import Surveys, Questions, Answers

register = template.Library()

@register.filter(name='qs_count')
def qs_count(value):
    id = int(value)
    res = Questions.objects.filter(survey_id=id).count()
    return res

@register.filter(name='qs_type')
def qs_type(value):
    qt = Questions.QUEST_TYPE
    res = ''
    for tt in qt:
        if value == tt[0]: res = tt[1]
    #print(f'{value} {type(value)}')
    return res

@register.filter(name='as_count')
def qs_count(value):
    id = int(value)
    #res = Answers.objects.filter(question_id=id).count()
    type = Questions.objects.get(id=id).type
    if type == '0':
        res = 'текст'
    else:
        res = Answers.objects.filter(question_id=id).count()
    return res
