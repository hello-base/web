# -*- coding: utf-8 -*-
import pytest

from components.events.models import Event, Performance, Venue
from components.events.factories import (EventFactory, PerformanceFactory,
    VenueFactory)

pytestmark = pytest.mark.django_db


class TestEvents:
    def test_factory(self):
        factory = EventFactory()
        assert isinstance(factory, Event)
        assert 'event' in factory.romanized_name


class TestPerformances:
    def test_factory(self):
        factory = PerformanceFactory()
        assert isinstance(factory, Performance)
        assert 'performance' in factory.romanized_name


class TestVenues:
    def test_factory(self):
        factory = VenueFactory()
        assert isinstance(factory, Venue)
        assert 'venue' in factory.romanized_name
