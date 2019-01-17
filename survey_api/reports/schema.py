
from survey_api.reports.models import SurveyQuestionTemplate, SurveyAnswer
from graphene import Node
from graphene import Int
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

class CustomNode(Node):
    class Meta:
        name = 'Node'

    @staticmethod
    def to_global_id(type, id):
        return id


class SurveyQuestionNode(DjangoObjectType):
    class Meta:
        model = SurveyQuestionTemplate
        interfaces = (CustomNode,)
        filter_fields = ['name']


class SurveyAnswerNode(DjangoObjectType):
    class Meta:
        model = SurveyAnswer
        interfaces = (CustomNode,)
        filter_fields = ['value']


class Query(object):
    question = Node.Field(SurveyQuestionNode)
    all_questions = DjangoFilterConnectionField(SurveyQuestionNode)

    answer = Node.Field(SurveyAnswerNode)
    all_answers = DjangoFilterConnectionField(SurveyAnswerNode)

    def resolve_all_questions(self, info, **kwargs):
        return SurveyQuestionTemplate.objects.all()

    def resolve_all_answers(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return SurveyAnswer.objects.select_related('question').all()
