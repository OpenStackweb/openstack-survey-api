from django.shortcuts import render
from django import http
import json
from survey_api.reports.models.survey_answer import SurveyAnswer, SurveyAnswerFilter
from survey_api.reports.models import SurveyTemplate, SurveyQuestionTemplate, Member, Continent, Survey
from django.db import models
from survey_api.reports.serializers import SurveySerializer, SurveyTemplateSerializer

# Create your views here.

def get_survey_data(request, survey_id):
    survey = Survey.objects.get(id=survey_id)

    if survey.survey_template.is_deployment() :
        survey = survey.entitysurvey.parent_survey

    json_result = SurveySerializer(survey).data
    data = json.dumps(json_result, indent=2)

    return http.HttpResponse(data, content_type="application/json")


def get_survey_templates(request):
    templates = SurveyTemplate.objects.all().filter(class_name='SurveyTemplate')

    json_result = SurveyTemplateSerializer(templates, many=True).data
    data = json.dumps(json_result, indent=2)

    return http.HttpResponse(data, content_type="application/json")

def answer_count(request):
    result = process_answer_count(request)

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
    items_result = [
        {'value': '0', 'value_count': 0},
        {'value': '1', 'value_count': 0},
        {'value': '2', 'value_count': 0},
        {'value': '3', 'value_count': 0},
        {'value': '4', 'value_count': 0},
        {'value': '5', 'value_count': 0},
        {'value': '6', 'value_count': 0},
        {'value': '7', 'value_count': 0},
        {'value': '8', 'value_count': 0},
        {'value': '9', 'value_count': 0},
        {'value': '10', 'value_count': 0},
    ]
    items = result.get('items');
    total = result.get('total');
    nps = {'D': 0, 'N': 0, 'P': 0, 'NPS': 0}

    for item in items:
        value = int(item.get('value'))
        value_count = int(item.get('value_count'))
        items_result[value]['value_count'] = value_count

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

    result['items'] = items_result
    result['extra'] = nps
    result['name'] = name

    #json answer
    data = json.dumps(result, indent=2)
    return http.HttpResponse(data, content_type="application/json")

def deployment_by_continent(request):
    name = request.GET.get('name', 'continent')
    result = process_answer_count(request)
    items = result.get('items')
    total = result.get('total')
    results_by_continent = {}
    continents = Continent.objects.prefetch_related('countries')

    for item in items:
        value = item.get('value')
        cont = continents.filter(countries__code=value).first()
        if not cont: continue

        if cont.id not in results_by_continent:
            results_by_continent[cont.id] = {'value':'', 'value_count': 0}

        results_by_continent[cont.id]['value'] = cont.name
        results_by_continent[cont.id]['value_count'] += item.get('value_count')

    for key, result in results_by_continent.items():
        percentage = round((int(result.get('value_count')) / total) * 100, 2)
        result['value_count'] = percentage

    items = list(results_by_continent.values())
    items = sorted(items, key=lambda item: item['value_count'], reverse=True)

    #json answer
    data = json.dumps({'name': name, 'items': items, 'total': total}, indent=2)
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
        items = [x for x in get_raw_data(request) if x.value != None]
        for obj in items:
            if not obj.value: continue
            for single_value in obj.value.split(','):
                if value_is_id:
                    if question.is_double_entry():
                        single_key = single_value
                        single_values = single_value.split(':')
                        first_value = value_templates.get(int(single_values[0])).get('value')
                        second_value = value_templates.get(int(single_values[1])).get('value')

                        single_value = first_value + '/' + second_value
                    else:
                        single_key = single_value
                        single_value = value_templates.get(int(single_value)).get('value')
                else:
                    single_key = single_value


                if single_key not in single_objects:
                    single_objects[single_key] = dict()
                    single_objects[single_key]['value_count'] = 0

                single_objects[single_key]['value'] = single_value
                single_objects[single_key]['value_count'] += 1

        items = list(single_objects.values())
    else:
        items = items.values('value').annotate(value_count=models.Count('step__survey'))
        items = [x for x in items if x.get('value') != None]

        if value_is_id:
            for obj in items:
                if not obj['value']: continue
                value_temp = value_templates.get(int(obj.get('value')))
                obj['value'] = value_temp.get('value')
                obj['order'] = int(value_temp.get('order'))

            if order == 'answer_display':
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
    order = request.GET.get('order', 'answer_display')

    template = SurveyTemplate.objects.get(id=template_id)

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
            if not obj.value: continue

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
                    owner_email = obj.step.survey.owner.email
                except Member.DoesNotExist:
                    owner = obj.step.survey.owner_id
                    owner_email = 'N/a'

                survey = obj.step.survey
                parent_survey_id = survey.id if not template.is_deployment() else survey.entitysurvey.parent_survey_id

                try:
                    company = SurveyAnswer.objects.get(step__survey_id=parent_survey_id, question__name='Organization').value
                except SurveyAnswer.DoesNotExist:
                    company = 'N/A'

                single_objects[single_value]['value'] = single_value
                single_objects[single_value]['surveys'].append({'name': owner, 'email': owner_email, 'id': survey.id, 'company': company})

        items = list(single_objects.values())
    else:
        answer_list = dict()

        for obj in items:
            if not obj.value: continue

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
                    owner_email = obj.step.survey.owner.email
                except Member.DoesNotExist:
                    owner = obj.step.survey.owner_id
                    owner_email = 'N/a'

                survey = obj.step.survey
                parent_survey = survey if not template.is_deployment() else survey.entitysurvey.parent_survey

                try:
                    company = SurveyAnswer.objects.get(step__survey_id=parent_survey.id, question__name='Organization').value
                except SurveyAnswer.DoesNotExist:
                    company = 'N/A'

                answer_list[the_value]['surveys'].append({'name': owner, 'email': owner_email, 'id': survey.id, 'company': company})

        items = list(answer_list.values())

    if order == 'answer_display':
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

