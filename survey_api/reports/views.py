from django.shortcuts import render
from django import http
import json
from survey_api.reports.models.survey_answer import SurveyAnswer, SurveyAnswerFilter
from survey_api.reports.models import SurveyTemplate, SurveyQuestionTemplate, Member
from django.core import serializers
from django.db import models

# Create your views here.

def answer_count(request):
    result = process_answer_count(request)

    # html answer
    #return render(request, 'answers_count.html', {'answers':items.get('items'), 'total': items.get('total')})

    #json answer
    data = json.dumps(result, indent=2)
    return http.HttpResponse(data, content_type="application/json")


def answer_percentage(request):
    result = process_answer_count(request)
    items = result.get('items')
    total = result.get('total')

    for item in items:
        percentage = round((int(item.get('value_count')) / total) * 100, 2)
        item['value_count'] = percentage

    #json answer
    data = json.dumps(result, indent=2)
    return http.HttpResponse(data, content_type="application/json")


def answer_list(request):
    result = process_answer_list(request)

    # json answer
    data = json.dumps(result, indent=2)
    return http.HttpResponse(data, content_type="application/json")

def nps(request):
    name = request.GET.get('name', 'nps')
    result = process_answer_count(request)
    items = result.get('items');
    total = result.get('total');
    nps = {'D': 0, 'N': 0, 'P': 0, 'NPS': 0}

    for item in items:
        value = int(item.get('value'))
        value_count = int(item.get('value_count'))

        if 0 <= value <= 6 :
            nps['D'] += value_count
        elif 7 <= value <= 8 :
            nps['N'] += value_count
        else :
            nps['P'] += value_count

    nps['D'] = round((nps['D']/total) * 100)
    nps['N'] = round((nps['N']/total) * 100)
    nps['P'] = round((nps['P']/total) * 100)
    nps['NPS'] = nps['P'] - nps['D']
    nps['D'] = str(nps['D']) + '%'
    nps['N'] = str(nps['N']) + '%'
    nps['P'] = str(nps['P']) + '%'

    result['extra'] = nps
    result['name'] = name

    #json answer
    data = json.dumps(result, indent=2)
    return http.HttpResponse(data, content_type="application/json")


def process_answer_count(request):
    name = request.GET.get('name', 'data')
    question_name = request.GET.get('question', '')
    template_id = request.GET.get('template', '')
    order = request.GET.get('order', 'count')

    question = SurveyQuestionTemplate.objects.get(name=question_name, step_template__survey_template_id=template_id)
    value_is_id = question.value_options.all().count();
    value_templates = dict()

    items = get_raw_data(request)
    total_count = items.count()

    if value_is_id:
        for value_temp in question.value_options.all().values():
            value_templates[value_temp.get('id')] = value_temp

    if question.is_multi_value():
        single_objects = dict()
        for obj in items:
            for single_value in obj.value.split(','):
                if value_is_id:
                    if question.is_double_entry():
                        single_values = single_value.split(':')
                        first_value = value_templates.get(int(single_values[0])).get('value')
                        second_value = value_templates.get(int(single_values[1])).get('value')

                        single_value = first_value + '/' + second_value
                    else:
                        single_value = value_templates.get(int(single_value)).get('value')

                if single_value not in single_objects:
                    single_objects[single_value] = dict()
                    single_objects[single_value]['value_count'] = 0

                single_objects[single_value]['value'] = single_value
                single_objects[single_value]['value_count'] += 1

        list(single_objects.values())
    else:
        items = items.values('value').annotate(value_count=models.Count('step__survey'))

        if value_is_id:
            for obj in items:
                value_temp = value_templates.get(int(obj.get('value')))
                obj['value'] = value_temp.get('value')
                obj['order'] = int(value_temp.get('order'))

            if order == 'value_order':
                items = sorted(items, key=lambda item: item.get('order'))

    if order == 'count':
        items = sorted(items, key=lambda item: item['value_count'], reverse=True)
    elif order == 'value':
        items = sorted(items, key=lambda item: item['value'])

    return {'name': name, 'items': items, 'total': total_count}


def process_answer_list(request):
    name = request.GET.get('name', 'data')
    question_name = request.GET.get('question', '')
    template_id = request.GET.get('template', '')
    order = request.GET.get('order', 'value_order')

    question = SurveyQuestionTemplate.objects.get(name=question_name, step_template__survey_template_id=template_id)
    value_is_id = question.value_options.all().count();
    value_templates = dict()

    items = get_raw_data(request)
    total_count = items.count()

    if value_is_id:
        for value_temp in question.value_options.all().values():
            value_templates[value_temp.get('id')] = value_temp

    if question.is_multi_value():
        single_objects = dict()
        for obj in items:
            for single_value in obj.value.split(','):
                if value_is_id:
                    if question.is_double_entry():
                        single_values = single_value.split(':')
                        first_value = value_templates.get(int(single_values[0])).get('value')
                        second_value = value_templates.get(int(single_values[1])).get('value')

                        single_value = first_value + '/' + second_value
                    else:
                        single_value = value_templates.get(int(single_value)).get('value')

                if single_value not in single_objects:
                    single_objects[single_value] = dict()
                    single_objects[single_value]['surveys'] = list()

                try:
                    owner = obj.step.survey.owner.full_name()
                except Member.DoesNotExist:
                    owner = obj.step.survey.owner_id

                single_objects[single_value]['value'] = single_value
                single_objects[single_value]['surveys'].append({'name': owner, 'id': obj.step.survey.id})

        items = list(single_objects.values())
    else:
        answer_list = dict()

        for obj in items:
            if value_is_id:
                value_temp = value_templates.get(int(obj.value))
                the_value = value_temp.get('value')
                the_order = value_temp.get('order')

                if the_value not in answer_list:
                    answer_list[the_value] = dict()
                    answer_list[the_value]['surveys'] = list()

                answer_list[the_value]['value'] = the_value
                answer_list[the_value]['order'] = int(the_order)

                try:
                    owner = obj.step.survey.owner.full_name()
                except Member.DoesNotExist:
                    owner = obj.step.survey.owner_id

                answer_list[the_value]['surveys'].append({'name': owner, 'id': obj.step.survey.id})

        items = list(answer_list.values())

    if order == 'value_order':
        items = sorted(items, key=lambda item: item['order'])
    else:
        items = sorted(items, key=lambda item: item['value'], reverse=True)

    # order each bundle by survey id
    for item in items:
        item['surveys'] = sorted(item['surveys'], key=lambda survey: survey['id'])

    return {'name': name, 'items': items, 'total': total_count}


def get_raw_data(request):
    template_id = request.GET.get('template', '')
    template = SurveyTemplate.objects.get(id=template_id)

    if template.is_deployment():
        f = SurveyAnswerFilter(request.GET, queryset=SurveyAnswer.objects.with_mandatory_answers())
    else:
        f = SurveyAnswerFilter(request.GET, queryset=SurveyAnswer.objects.with_deployment())

    return f.qs