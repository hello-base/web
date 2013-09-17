import datetime
from django.conf import settings

CLIENT_ID = settings.HELLO_BASE_CLIENT_ID
CLIENT_SECRET = settings.HELLO_BASE_CLIENT_SECRET
AUTHORIZATION_URL = settings.OAUTH_AUTHORIZATION_URL
ACCESS_TOKEN_URL = settings.ACCESS_TOKEN_URL
REFRESH_TOKEN_URL = settings.REFRESH_TOKEN_URL
REDIRECT_URL = settings.OAUTH_REDIRECT_URL
MEISHI_ENDPOINT = settings.MEISHI_ENDPOINT


class Meishi(object):
    def refresh_token_if_necessary(self, user):
        if datetime.datetime.now() > user.token_expiration:
            # Fetch a new token.
            base = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URL, state=request.GET['state'])
            token = base.fetch_token(REFRESH_TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), token=user.refresh_token)
            user.access_token = token['access_token']
            user.refresh_token = token['refresh_token']
            user.token_expiration = token['expires_in']
            user.save()
        return user

    def get(self, path, user):
        user = self.refresh_token_if_necessary(user)
        session = OAuth2Session(self.client_id, token=user.access_token)
        return session.get('%s%s' % (MEISHI_ENDPOINT, path).json()
