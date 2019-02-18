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
from .country import Country

class Continent(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=50)
    countries = models.ManyToManyField(Country, through='ContinentCountries', through_fields=('continent_id', 'country_code'))

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'reports'
        db_table = 'Continent'


class ContinentCountries(models.Model):
    continent_id = models.ForeignKey(Continent, db_column='ContinentID', on_delete=models.CASCADE)
    country_code = models.ForeignKey(Country, db_column='CountryCode', on_delete=models.CASCADE)

    def __str__(self):
        return self.continent_id + ' - ' + self.country_code

    class Meta:
        app_label = 'reports'
        db_table = 'Continent_Countries'