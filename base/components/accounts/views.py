from django.conf import settings
from django.views.generic import RedirectView, View

from requests_oauthlib import OAuth2Session


CLIENT_ID = settings.get('HELLO_BASE_CLIENT_ID', '')
CLIENT_SECRET = settings.get('HELLO_BASE_CLIENT_SECRET', '')
AUTHORIZATION_URL = 'http://localhost:8002/authorize'
TOKEN_URL = 'http://localhost:8002/token'

class PreAuthorizationView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # Redirect the user to Hello! Base ID using the appropriate
        # URL with a few key OAuth paramters built in.
        base = OAuth2Session(CLIENT_ID)
        authorization_url, state = base.authorization_url(AUTHORIZATION_URL)

        # State is used to prevent CSRF, so let's keep this for later.
        self.request.session['oauth_state'] = state
        return authorization_url


class PostAuthorizationView(View):
    def get(self, request, *args, **kwargs):
        base = OAuth2Session(CLIENT_ID, state=self.request.session['oauth_state'])
        token = base.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=self.request.url)


