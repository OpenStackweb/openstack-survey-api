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



"""survey_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from graphene_django.views import GraphQLView

from survey_api.reports import views

urlpatterns = [
    path('reports', GraphQLView.as_view(graphiql=True)),
    path('survey-templates', views.get_survey_templates),
    path('survey/<int:survey_id>', views.get_survey_data),
    path('answers/count', views.answer_count),
    path('answers/percentage', views.answer_percentage),
    path('answers/list', views.answer_list),
    path('answers/nps', views.nps),
    path('answers/deployment-by-continent', views.deployment_by_continent)
]
