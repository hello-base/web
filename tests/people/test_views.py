import pytest

from django.core.urlresolvers import reverse

from base.apps.people import factories


@pytest.mark.django_db
def test_group_detail_view(client):
    group = factories.GroupFactory()
    response = client.get(reverse('group-detail', kwargs={'slug': group.slug}))
    assert response.status_code == 200
    assert 'object' in response.context
    assert 'people/group_detail.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_idol_detail_view(client):
    idol = factories.IdolFactory()
    response = client.get(reverse('idol-detail', kwargs={'slug': idol.slug}))
    assert response.status_code == 200
    assert 'object' in response.context
    assert 'people/idol_detail.html' in [template.name for template in response.templates]
