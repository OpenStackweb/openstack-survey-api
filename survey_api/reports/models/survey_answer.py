"""
 * Copyright 2019 OpenStack Foundation
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
"""

from django.db import models
from .survey_question_template import SurveyQuestionTemplate
from .survey_question_value_template import SurveyQuestionValueTemplate
from .survey_step import SurveyStep
from .survey_template import SurveyTemplate
from .continent import Continent
import django_filters
from django.db.models import Exists, OuterRef, Q
from functools import reduce

class SurveyAnswerManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(SurveyAnswerManager, self).get_queryset().filter(step__survey__is_test=0)

    def with_deployment(self):
        deployment_filter = SurveyAnswer.objects.filter(step__survey__entitysurvey__parent_survey_id=OuterRef('step__survey_id'), question__is_mandatory=1)
        return self.get_queryset().annotate(has_deployment=Exists(deployment_filter)).filter(has_deployment=True)

    def with_mandatory_answers(self):
        mandatory_filter = SurveyAnswer.objects.filter(step__survey_id=OuterRef('step__survey_id'), question__is_mandatory=1)
        return self.get_queryset().annotate(has_mandatory=Exists(mandatory_filter)).filter(has_mandatory=True)

class SurveyAnswer(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    value = models.TextField(null=True, db_column='Value')
    question = models.ForeignKey(
        SurveyQuestionTemplate, related_name='answers', db_column='QuestionID', on_delete=models.CASCADE)
    step = models.ForeignKey(
        SurveyStep, related_name='answers', db_column='StepID', on_delete=models.CASCADE)

    objects = SurveyAnswerManager()

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'SurveyAnswer'



class SurveyAnswerFilter(django_filters.FilterSet):
    value = django_filters.CharFilter(field_name='value')
    question = django_filters.CharFilter(field_name='question__name')
    template = django_filters.NumberFilter(field_name='question__step_template__survey_template__id')
    country = django_filters.CharFilter(method='country_filter')
    continent = django_filters.CharFilter(method='continent_filter')
    language = django_filters.CharFilter(field_name='step__survey__lang')
    answer = django_filters.CharFilter(method='answer_filter')
    answer_gt = django_filters.CharFilter(method='answer_filter_gt')

    date = django_filters.DateFromToRangeFilter(field_name='step__survey__last_edited')
    #&date_after=2018-07-22&date_before=2019-02-01


    class Meta:
        model = SurveyAnswer
        fields = ['value', 'question']


    def country_filter(self, queryset, name, value):
        template = SurveyTemplate.objects.get(id=self.data.get('template'))
        survey_ref = 'step__survey__entitysurvey__parent_survey_id' if not template.is_deployment() else 'step__survey_id'

        answer_exists = SurveyAnswer.objects\
            .filter(**{survey_ref: OuterRef('step__survey_id'), 'question__name': 'CountriesPhysicalLocation'})\
            .extra(where=['FIND_IN_SET(%s, Value) > 0'], params=[str(value)])

        return queryset.annotate(country_filter=Exists(answer_exists)).filter(country_filter=True)

    def continent_filter(self, queryset, name, value):
        countries = list(Continent.objects.filter(name=value).first().countries.values_list('code', flat=True))

        answer_exists = SurveyAnswer.objects\
            .filter(step__survey_id=OuterRef('step__survey__entitysurvey__parent_survey_id'), question__name__startswith='PrimaryCountry', value__in=countries)

        queryset = queryset.annotate(continent_filter=Exists(answer_exists)).filter(continent_filter=True)
        return queryset

    def answer_filter(self, queryset, name, value):
        filter_value = value.split(',')
        question = filter_value[0]
        answer = filter_value[1]

        answer_exists = SurveyAnswer.objects \
            .filter(step__survey_id=OuterRef('step__survey_id'), question_id=question) \
            .extra(where=['FIND_IN_SET(%s, Value) > 0'], params=[str(answer)])

        queryset = queryset.annotate(answer_filter=Exists(answer_exists)).filter(answer_filter=True)
        return queryset

    def answer_filter_gt(self, queryset, name, value):
        filter_value = value.split(',')
        question = filter_value[0]
        answer = filter_value[1]

        answer_filter = SurveyQuestionValueTemplate.objects.get(id=answer)
        answer_options = list(SurveyQuestionValueTemplate.objects.filter(question_id=question, order__gt=answer_filter.order).order_by('order').values_list('id', flat=True))

        answer_exists = SurveyAnswer.objects \
            .filter(step__survey_id=OuterRef('step__survey_id'), question_id=question) \
            .filter(reduce(lambda x, y: x | y, [Q(value=item) for item in answer_options]))

        queryset = queryset.annotate(answer_filter=Exists(answer_exists)).filter(answer_filter=True)
        return queryset