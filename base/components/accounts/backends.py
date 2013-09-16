from django.contrib.auth import get_user_model

from oauthlib.oauth2.rfc6749.endpoints import resource


USER = get_user_model()

class OAuth2Backend(object):
    """
    Authenticate against an OAuth2 access token.

    """
    def authenticate(self, **credentials):
        request = credentials.get('request')
        if request is not None:
            is_valid, request = resource.verify_request(request, scopes=[])
            if is_valid:
                return request.user
        return None

    def get_user(self, user_id):
        try:
            return USER.objects.get(pk=user_id)
        except USER.DoesNotExist:
            return None
