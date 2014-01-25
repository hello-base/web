# -*- coding: utf-8 -*-
import pytest

from components.events.models import Activity, Event, Venue
from components.events.factories import (ActivityFactory, EventFactory,
    VenueFactory)

pytestmark = pytest.mark.django_db


class TestEvents:
    def test_factory(self):
        factory = EventFactory()
        assert isinstance(factory, Event)
        assert 'event' in factory.romanized_name

    def test_get_absolute_url(self, client):
        factory = EventFactory()
        response = client.get(factory.get_absolute_url())
        assert response.status_code == 200


class TestActivities:
    def test_factory(self):
        factory = ActivityFactory()
        assert isinstance(factory, Activity)
        assert 'activity' in factory.romanized_name


class TestVenues:
    def test_factory(self):
        factory = VenueFactory()
        assert isinstance(factory, Venue)
        assert 'venue' in factory.romanized_name

    def test_get_absolute_url(self, client):
        factory = VenueFactory()
        response = client.get(factory.get_absolute_url())
        assert response.status_code == 200
