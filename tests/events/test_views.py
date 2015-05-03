import pytest

from django.core.urlresolvers import reverse

from apps.events import factories


@pytest.mark.django_db
def test_event_detail_view(client):
    group = factories.EventFactory()
    response = client.get(reverse('event-detail', kwargs={'slug': group.slug}))
    assert response.status_code == 200
    assert 'object' in response.context
    assert 'events/event_detail.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_venue_detail_view(client):
    idol = factories.VenueFactory()
    response = client.get(reverse('venue-detail', kwargs={'slug': idol.slug}))
    assert response.status_code == 200
    assert 'object' in response.context
    assert 'events/venue_detail.html' in [template.name for template in response.templates]
