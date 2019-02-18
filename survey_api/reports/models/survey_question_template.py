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


class SurveyQuestionTemplate(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    class_name = models.CharField(db_column='ClassName', max_length=50, null=True)
    name = models.TextField(db_column='Name')
    is_mandatory = models.BooleanField(db_column='Mandatory')
    step_template = models.ForeignKey(
        SurveyStepTemplate, related_name='questions', db_column='StepID', on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    def is_double_entry(self):
        return self.class_name == 'SurveyRadioButtonMatrixTemplateQuestion'

    def is_multi_value(self):
        if self.class_name == 'SurveyDropDownQuestionTemplate':
            return self.surveydropdownquestiontemplate.is_multi_value
        else:
            classes = [
                'SurveyRankingQuestionTemplate',
                'SurveyCheckBoxListQuestionTemplate',
                'SurveyRadioButtonMatrixTemplateQuestion'
            ]

            return self.class_name in classes

    def is_country_selector(self):
        if self.class_name == 'SurveyDropDownQuestionTemplate':
            return self.surveydropdownquestiontemplate.is_country_selector
        else:
            return False

    class Meta:
        app_label = 'reports'
        db_table = 'SurveyQuestionTemplate'