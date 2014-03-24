# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import http
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import RedirectView, View

from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

from .api import auth_session, auth_url, auth_token

User = get_user_model()


class PreAuthorizationView(RedirectView):
    def get_authorization_url(self, request):
        # Redirect the user to Hello! Base ID using the appropriate URL with
        # a few key OAuth paramters built in. We throw in
        # `request.META['HTTP_REFERER']` as a way to redirect back to the
        # referring page when we're done.
        oauth = auth_session(request)
        authorization_url, state = auth_url(oauth)

        # In order to persist "session values" from an AnonymousUser to a
        # logged in user, we need to use cookies.
        redirect = http.HttpResponseRedirect(authorization_url)
        redirect.set_cookie('oauth_referrer', request.META.get('HTTP_REFERER', ''))
        redirect.set_cookie('oauth_state', state)
        return redirect

    def get(self, request, *args, **kwargs):
        return self.get_authorization_url(request)


class PostAuthorizationView(View):
    def get_token(self, session, redirect_uri):  # pragma: no cover
        try:
            token = auth_token(session, redirect_uri)
        except InvalidGrantError:  # Whoops, try again.
            return http.HttpResponseRedirect(reverse('oauth-authorize'))
        return token

    def get_profile(self, session):  # pragma: no cover
        # Hooray! Somebody sent us up the token.
        # Now let's fetch their user from the Hello! Base ID API.
        r = session.get('%s%s' % (settings.MEISHI_ENDPOINT, 'user/'))
        r.raise_for_status()
        return r.json()

    def process_user(self, profile, token):
        # We have the profile data, let's check for an existing user.
        # If we don't have one, create one.
        try:
            user = User.objects.get(base_id=profile['id'])
        except User.DoesNotExist:
            user = User.objects.create_user(
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
        return user

    def get(self, request, *args, **kwargs):
        # Take the state from the cookie and try to get ourselves a token.
        oauth = auth_session(request, state=request.COOKIES['oauth_state'])
        token = self.get_token(oauth, kwargs.get('redirect_uri', request.build_absolute_uri()))
        profile = self.get_profile(oauth)

        # Now let's try to log in.
        user = self.process_user(profile, token)
        user = authenticate(username=user.username)
        login(request, user)

        # If login has succeeded (which it probably has), then redirect
        # the user to the page they initiated login on and delete the
        # appropriate cookies.
        if 'oauth_referrer' in request.COOKIES and request.COOKIES['oauth_referrer'] != '':
            redirect = http.HttpResponseRedirect(request.COOKIES['oauth_referrer'])
            redirect.delete_cookie('oauth_state')
            redirect.delete_cookie('oauth_referrer')
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
