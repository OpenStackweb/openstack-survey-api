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
from .survey_step_template import SurveyStepTemplate
from .survey import Survey


class SurveyStep(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    state = models.CharField(db_column='State', max_length=50)
    class_name = models.CharField(db_column='ClassName', max_length=50, null=True)
    step_template = models.ForeignKey(
        SurveyStepTemplate, related_name='steps', db_column='TemplateID', on_delete=models.CASCADE)
    survey = models.ForeignKey(
        Survey, related_name='steps', db_column='SurveyID', on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'SurveyStep'