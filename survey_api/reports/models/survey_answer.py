from django.db import models
from .survey_question_template import SurveyQuestionTemplate



class SurveyAnswer(models.Model):
    value = models.TextField(null=True, db_column='Value')
    question = models.ForeignKey(
        SurveyQuestionTemplate, related_name='answers', db_column='QuestionID', on_delete=models.CASCADE)

    def __str__(self):
        return self.value

    class Meta:
        app_label = 'reports'
        db_table = 'SurveyAnswer'