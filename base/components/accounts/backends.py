from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from oauthlib.oauth2.rfc6749.endpoints import resource


USER = get_user_model()

class HelloBaseIDBackend(ModelBackend):
    def authenticate(self, username=None):
        try:
            user = USER.objects.filter(username=username)[0]
        except IndexError:
            return None
        else:
            return user

    def get_user(self, user_id):
        try:
            return USER.objects.get(pk=user_id)
        except USER.DoesNotExist:
            return None
