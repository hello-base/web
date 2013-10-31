import pytest

from django.core.urlresolvers import reverse

from components.accounts.factories import EditorFactory
from components.accounts.views import (PreAuthorizationView,
    PostAuthorizationView)


def test_preauthorization_view(rf):
    request = rf.get(reverse('oauth-authorize'))
    response = PreAuthorizationView.as_view()(request)
    assert response.cookies['oauth_state']
    assert response.status_code == 302
    assert 'response_type=code' in response.serialize()
