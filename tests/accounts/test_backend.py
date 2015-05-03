# -*- coding: utf-8 -*-
import pytest

from django.conf import settings
from django.contrib.auth import get_user_model, get_user
from django.http import HttpRequest

from apps.accounts.factories import EditorFactory

pytestmark = pytest.mark.django_db
User = settings.AUTH_USER_MODEL


def test_authentication(client):
    editor = EditorFactory(base_id=1, is_active=True, username='bryan')
    assert client.login(username=editor.username)

    request = HttpRequest()
    request.session = client.session
    user = get_user(request)
    assert user is not None
    assert not user.is_anonymous()


def test_failing_authentication(client):
    assert not client.login(username='bryan')

    request = HttpRequest()
    request.session = client.session
    user = get_user(request)
    assert user is not None
    assert user.is_anonymous()
