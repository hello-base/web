from django import http
from django.conf import settings
from django.views.generic import RedirectView, View

from requests_oauthlib import OAuth2Session


CLIENT_ID = settings.HELLO_BASE_CLIENT_ID
CLIENT_SECRET = settings.HELLO_BASE_CLIENT_SECRET
AUTHORIZATION_URL = 'https://localhost:8443/authorize/'
TOKEN_URL = 'https://localhost:8443/token/'

class PreAuthorizationView(RedirectView):
    def get(self, request, *args, **kwargs):
        # Redirect the user to Hello! Base ID using the appropriate
        # URL with a few key OAuth paramters built in.
        base = OAuth2Session(CLIENT_ID)
        authorization_url, state = base.authorization_url(AUTHORIZATION_URL)

        # State is used to prevent CSRF, so let's keep this for later.
        request.session['oauth_state'] = state
        request.session.modified = True
        return http.HttpResponseRedirect(authorization_url)


class PostAuthorizationView(View):
    def get(self, request, *args, **kwargs):
        # We SHOULD be grabbing state from the session, maybe this'll
        # work in production, but in development it's not. So... we're
        # doing this. :(
        base = OAuth2Session(CLIENT_ID, state=request.GET['state'])
        token = base.fetch_token(
            TOKEN_URL,
            auth=(CLIENT_ID, CLIENT_SECRET),
            authorization_response=request.build_absolute_uri()
        )


