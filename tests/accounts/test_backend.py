import pytest

from django.contrib.auth import get_user
from django.http import HttpRequest
from django.core import mail

from components.accounts.factories import EditorFactory

pytestmark = pytest.mark.django_db


def test_authentication_backend(client):
    editor = EditorFactory(base_id=1, is_active=True, username='bryan')
    assert client.login(username=editor.username)

    request = HttpRequest()
    request.session = client.session
    user = get_user(request)
    assert user is not None
    assert not user.is_anonymous()
