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


from django.http import HttpResponseForbidden, HttpResponse
from django.conf import settings
from survey_api.reports.models import OAuthToken
import requests, logging, time


class TokenValidationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # skip auth
        return self.get_response(request)

        if not 'access_token' in request.GET :
            return HttpResponseForbidden()

        access_token = request.GET.get('access_token')

        if not access_token:
            logging.getLogger('django').error('INVALID TOKEN')
            return HttpResponseForbidden()


        # try get access_token from DB and check if not expired
        db_access_token = OAuthToken.objects.filter(token = access_token).first()

        if db_access_token is not None :
            if db_access_token.expiration_date > time.time() :
                return self.get_response(request)
            else :
                db_access_token.delete()


        # Token instrospection
        response = requests.post(
            'https://testopenstackid.openstack.org/oauth2/token/introspection',
            auth=(settings.RS_CLIENT_ID,settings.RS_CLIENT_SECRET),
            params={'token' : access_token}
        )

        #print(response.text)

        if response.status_code == requests.codes.ok :
            token_info = response.json()
            new_token = OAuthToken.create(token_info)
            new_token.save()
        else :
            logging.getLogger('django').error('INVALID TOKEN')
            return HttpResponseForbidden()


        return self.get_response(request)



