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


class SurveyQuestionValueTemplate(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    value = models.TextField(db_column='Value')
    label = models.TextField(db_column='Label')
    order = models.IntegerField(db_column='Order')
    question = models.ForeignKey(
        SurveyQuestionTemplate, related_name='value_options', db_column='OwnerID', on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'SurveyQuestionValueTemplate'