# -*- coding: utf-8 -*-
import pytest

from apps.accounts import api
from apps.accounts.factories import EditorFactory


@pytest.fixture
def token():
    return {
        'access_token': 'eswfld123kjhn1v5423',
        'refresh_token': 'asdfkljh23490sdf',
        'token_type': 'Bearer',
        'expires_in': 3600
    }


@pytest.fixture
def expires_at_token():
    return {
        'access_token': 'eswfld123kjhn1v5423',
        'refresh_token': 'asdfkljh23490sdf',
        'token_type': 'Bearer',
        'expires_at': 1383209373.147299
    }


def test_token_updater_with_no_user(token, rf):
    api._token_updater(token, rf)(token)
    assert token['access_token'] == 'eswfld123kjhn1v5423'
    assert isinstance(token['expires_at'], int)


@pytest.mark.django_db
def test_token_updater_with_user(token, rf):
    user = EditorFactory()
    rf.user = user
    api._token_updater(token, rf)(token)
    assert token['access_token'] == 'eswfld123kjhn1v5423'
    assert isinstance(token['expires_at'], int)
    assert user.access_token == 'eswfld123kjhn1v5423'
    assert isinstance(user.token_expiration, int)
