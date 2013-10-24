import pytest

from django.core.urlresolvers import reverse


def test_site_view(client):
    response = client.get(reverse('site-home'))
    assert response.status_code == 200
    assert 'landings/home_site.html' in [template.name for template in response.templates]
