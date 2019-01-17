from django.db import models
import time


class OAuthToken(models.Model):
    token = models.TextField(null=True)
    scopes = models.TextField()
    expiration_date = models.IntegerField()

    def __str__(self):
        return self.token

    @classmethod
    def create(cls, token_info):
        expiration = time.time() + token_info['expires_in']
        token = cls(token=token_info['access_token'], scopes=token_info['scope'], expiration_date=expiration)
        # do something with the token
        return token

    class Meta:
        app_label = 'auth'
        db_table = 'OAuthToken'