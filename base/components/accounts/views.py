from django import http
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.utils import timezone
from django.views.generic import RedirectView, View

from requests_oauthlib import OAuth2Session


USER = get_user_model()
CLIENT_ID = settings.HELLO_BASE_CLIENT_ID
CLIENT_SECRET = settings.HELLO_BASE_CLIENT_SECRET
AUTHORIZATION_URL = settings.OAUTH_AUTHORIZATION_URL
TOKEN_URL = settings.OAUTH_TOKEN_URL
REDIRECT_URL = settings.OAUTH_REDIRECT_URL

class PreAuthorizationView(RedirectView):
    def get(self, request, *args, **kwargs):
        # Redirect the user to Hello! Base ID using the appropriate
        # URL with a few key OAuth paramters built in. We throw in
        # `request.META['HTTP_REFERER']` as a way to redirect back to
        # the referring page when we're done.
        base = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URL)
        authorization_url, state = base.authorization_url(AUTHORIZATION_URL)

        # In order to persist "session values" from an AnonymousUser
        # to a logged in user, we need to use cookies.
        redirect = http.HttpResponseRedirect(authorization_url)
        redirect.set_cookie('oauth_referrer', request.META.get('HTTP_REFERER', ''))
        redirect.set_cookie('oauth_state', state)
        return redirect


class PostAuthorizationView(View):
    def get(self, request, *args, **kwargs):
        # We SHOULD be grabbing state from the session, maybe this'll
        # work in production, but in development it's not. So... we're
        # doing this. :(
        base = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URL, state=request.COOKIES['oauth_state'])
        token = base.fetch_token(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), authorization_response=request.build_absolute_uri())

        # Hooray! Somebody sent us up the token.
        # Now let's fetch their user from the Hello! Base ID API.
        hbi = OAuth2Session(CLIENT_ID, token=token)
        profile = hbi.get('%s%s' % (settings.MEISHI_ENDPOINT, 'user/')).json()
        print profile

        # Now that we have the profile data, let's check for an
        # existing user. If we don't have one, create one.
        try:
            user = USER.objects.get(base_id=profile['id'])
        except USER.DoesNotExist:
            user = USER.objects.create_user(
                username=profile['username'],
                email=profile['email'],
                base_id=profile['id'],
            )
        user.username = profile['username']
        user.name = profile['display_name']
        user.email = profile['email']
        user.is_active = profile['is_active']
        user.is_staff = profile['is_staff']
        user.is_superuser = profile['is_superuser']
        user.access_token = token['access_token']
        user.refresh_token = token['refresh_token']
        user.token_expiration = token['expires_in']
        user.active_since = timezone.now()
        user.save()

        # Now let's try to log in.
        user = authenticate(username=profile['username'])
        login(request, user)

        # If login has succeeded (which it probably has), then redirect
        # the user to the page they initiated login on and delete the
        # appropriate cookies.
        if 'oauth_referrer' in request.COOKIES and request.COOKIES['oauth_referrer'] != '':
            redirect = http.HttpResponseRedirect(request.COOKIES['oauth_referrer'])
            redirect.delete_cookie('oauth_state')
            redirect.delete_cookie('oauth_referrer')
            return redirect
        else:
            redirect = http.HttpResponseRedirect('/')
            redirect.delete_cookie('oauth_state')
            return redirect


class QuicklinksMixin(object):
    def get_context_data(self, **kwargs):
        # Activates quicklinks to the administration system.
        context = super(QuicklinksMixin, self).get_context_data(**kwargs)
        context['opts'] = self.object._meta
        return context
