import pytest

from django.contrib.auth import get_user_model, get_user
from django.http import HttpRequest
from django.core import mail

from components.accounts.factories import EditorFactory

pytestmark = pytest.mark.django_db
User = get_user_model()


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
