from django import http
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import RedirectView, View

from requests_oauthlib import OAuth2Session

from .api import auth_session, auth_url, auth_token


USER = get_user_model()

class PreAuthorizationView(RedirectView):
    def get(self, request, *args, **kwargs):
        # Redirect the user to Hello! Base ID using the appropriate
        # URL with a few key OAuth paramters built in. We throw in
        # `request.META['HTTP_REFERER']` as a way to redirect back to
        # the referring page when we're done.
        oauth = auth_session(request)
        authorization_url, state = auth_url(oauth)

        # In order to persist "session values" from an AnonymousUser
        # to a logged in user, we need to use cookies.
        redirect = http.HttpResponseRedirect(authorization_url)
        redirect.set_cookie('oauth_referrer', request.META.get('HTTP_REFERER', ''))
        redirect.set_cookie('oauth_state', state)
        return redirect


class PostAuthorizationView(View):
    def get(self, request, *args, **kwargs):
        # Take the state from the cookie and try to get ourselves a token.
        oauth = auth_session(request, state=request.COOKIES['oauth_state'])

        try:
            token = auth_token(oauth, request.build_absolute_uri())
        except InvalidGrantError:  # Whoops, try again.
            return http.HttpResponseRedirect(reverse('oauth-authorize'))

        # Hooray! Somebody sent us up the token.
        # Now let's fetch their user from the Hello! Base ID API.
        r = oauth.get('%s%s' % (settings.MEISHI_ENDPOINT, 'user/'))
        r.raise_for_status()
        profile = r.json()

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
        user.token_expiration = token['expires_at']
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
