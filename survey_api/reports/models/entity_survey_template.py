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

class EntitySurveyTemplate(SurveyTemplate):
    parent_template = models.ForeignKey(
        SurveyTemplate, related_name='entity_surveys', db_column='ParentID', on_delete=models.CASCADE)
    surveytemplate_ptr = models.OneToOneField(
        SurveyTemplate, on_delete=models.CASCADE, parent_link=True, db_column='ID')

    class Meta:
        app_label = 'reports'
        db_table = 'EntitySurveyTemplate'