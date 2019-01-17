from django.http import HttpResponseForbidden, HttpResponse
from django.conf import settings
from survey_api.reports.models import OAuthToken
import requests, logging, time


class TokenValidationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not 'accessToken' in request.GET :
            return HttpResponseForbidden()

        access_token = request.GET.get('accessToken')

        if not access_token:
            logging.getLogger('django').error('INVALID TOKEN')
            return HttpResponseForbidden()


        # try get AccessToken from DB and check if not expired
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

        if response.status_code == requests.codes.ok :
            token_info = response.json()
            new_token = OAuthToken.create(token_info)
            new_token.save()
        else :
            logging.getLogger('django').error('INVALID TOKEN')
            return HttpResponseForbidden()


        return self.get_response(request)



