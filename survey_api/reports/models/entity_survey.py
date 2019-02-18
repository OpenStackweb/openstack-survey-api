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
from .survey import Survey


class EntitySurvey(Survey):
    parent_survey = models.ForeignKey(
        Survey, related_name='entity_surveys', db_column='ParentID', on_delete=models.CASCADE)
    survey_ptr = models.OneToOneField(
        Survey, on_delete=models.CASCADE, parent_link=True, db_column='ID')

    def get_country(self):
        return self.parent_survey.get_country(self.parent_survey)

    def get_continent(self):
        return self.parent_survey.get_continent(self.parent_survey)

    class Meta:
        app_label = 'reports'
        db_table = 'EntitySurvey'