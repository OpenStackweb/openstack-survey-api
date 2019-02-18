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

from survey_api.reports.models import SurveyQuestionTemplate, SurveyQuestionValueTemplate, SurveyAnswer, SurveyTemplate
from graphene import relay, String, Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

class CustomNode(relay.Node):
    class Meta:
        name = 'Node'

    @staticmethod
    def to_global_id(type, id):
        return id


class SurveyTemplateNode(DjangoObjectType):
    class Meta:
        model = SurveyTemplate
        filter_fields = ['id','title']
        interfaces = (CustomNode, )

class SurveyQuestionNode(DjangoObjectType):
    class Meta:
        model = SurveyQuestionTemplate
        filter_fields = ['id','name','answers']
        interfaces = (CustomNode,)


class SurveyAnswerNode(DjangoObjectType):
    class Meta:
        model = SurveyAnswer
        filter_fields = [
            'value',
            'question__id'
        ]
        interfaces = (CustomNode,)


    get_value = String()
    def resolve_get_value(instance, info, **kwargs):
        return instance.get_value()


class Query(object):
    all_questions = DjangoFilterConnectionField(SurveyQuestionNode)
    all_answers = DjangoFilterConnectionField(SurveyAnswerNode)

    #survey_answers_to_question = DjangoFilterConnectionField(SurveyAnswerNode)
    #
    # def resolve_all_questions(self, info, **kwargs):
    #     return SurveyQuestionTemplate.objects.all()
    #
    # def resolve_all_answers(self, info, **kwargs):
    #     return SurveyAnswer.objects.select_related('question').all()

    # def resolve_survey_answers_to_question(self, info, templateId, questionId):
    #     query = SurveyAnswer.objects.all()
    #
    #     return query.filter(id=questionId, step_survey_teplate_id=templateId)
