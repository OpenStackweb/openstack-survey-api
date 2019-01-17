from django.contrib import admin
from survey_api.reports.models import SurveyQuestionTemplate, SurveyAnswer, OAuthToken


# Register models here

admin.site.register(SurveyQuestionTemplate)
admin.site.register(SurveyAnswer)
admin.site.register(OAuthToken)