from django.db import models



class SurveyQuestionTemplate(models.Model):
    name = models.CharField(max_length=100, db_column='Name')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'reports'
        db_table = 'SurveyQuestionTemplate'