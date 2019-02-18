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
from .survey_template import SurveyTemplate
from .member import Member
from pycountry_convert import country_alpha2_to_continent_code


class SurveyManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(SurveyManager, self).get_queryset().filter(is_test=0)

class Survey(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    class_name = models.TextField(db_column='ClassName', max_length=50, null=True)
    is_test = models.BooleanField(db_column='IsTest')
    state = models.CharField(db_column='State', max_length=50)
    lang = models.CharField(db_column='Lang', max_length=10)
    last_edited = models.DateTimeField(db_column='LastEdited')
    survey_template = models.ForeignKey(
        SurveyTemplate, related_name='surveys', db_column='TemplateID', on_delete=models.CASCADE)
    owner = models.ForeignKey(
        Member, related_name='surveys', db_column='CreatedByID', on_delete=models.CASCADE)

    objects = SurveyManager()

    def __str__(self):
        return self.id

    def get_country(self):
        answer = self.steps.answers.filter(question__name='CountriesPhysicalLocation').first()
        return answer.value

    def get_continent(self):
        country = self.get_country(self)
        return country_alpha2_to_continent_code(country)


    class Meta:
        app_label = 'reports'
        db_table = 'Survey'