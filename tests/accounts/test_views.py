# -*- coding:utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from apps.accounts.views import (PreAuthorizationView,
    PostAuthorizationView)
from tests.utils import add_session_to_request, setup_view


def mock_token(session, redirect_uri):
    return {
        'access_token': 'eswfld123kjhn1v5423',
        'refresh_token': 'asdfkljh23490sdf',
        'token_type': 'Bearer',
        'expires_at': 1383209373.147299
    }


def mock_profile(oauth):
    return {
        'id': 1,
        'username': 'bryan',
        'display_name': 'Bryan',
        'email': 'bryan@hello-base.com',
        'is_active': True,
        'is_staff': True,
        'is_superuser': True
    }


def test_pre_authorization_view(rf):
    request = rf.get(reverse('oauth-authorize'))
    response = PreAuthorizationView.as_view()(request)
    assert response.cookies['oauth_state']
    assert response.status_code == 302
    assert 'response_type=code' in response.serialize()


@pytest.mark.django_db
def test_post_authorization_view(rf, monkeypatch):
    view = PostAuthorizationView()
    monkeypatch.setattr(view, 'get_token', mock_token)
    monkeypatch.setattr(view, 'get_profile', mock_profile)

    # Prepare the RequestFactory, give it a session and throw it a cookie.
    request = rf.get(reverse('oauth-callback'))
    request = add_session_to_request(request)
    request.COOKIES['oauth_state'] = 'state'
    request.COOKIES['oauth_referrer'] = '/profile/'

    view = setup_view(view, request)
    response = view.dispatch(view.request, *view.args, **view.kwargs)
    assert response.status_code == 302


@pytest.mark.django_db
def test_post_authorization_view_with_no_redirect(rf, monkeypatch):
    view = PostAuthorizationView()
    monkeypatch.setattr(view, 'get_token', mock_token)
    monkeypatch.setattr(view, 'get_profile', mock_profile)

    # Prepare the RequestFactory, give it a session and throw it a cookie.
    request = rf.get(reverse('oauth-callback'))
    request = add_session_to_request(request)
    request.COOKIES['oauth_state'] = 'state'

    view = setup_view(view, request)
    response = view.dispatch(view.request, *view.args, **view.kwargs)
    assert response.status_code == 302
