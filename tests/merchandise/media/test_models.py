# -*- coding: utf-8 -*-
import pytest

from components.merchandise.media.factories import VideodiscFactory
from components.merchandise.media.models import Videodisc

pytestmark = pytest.mark.django_db


class TestVideodiscs:
    def test_factory(self):
        factory = VideodiscFactory()
        assert isinstance(factory, Videodisc)

    def test_get_absolute_url(self, client):
        factory = VideodiscFactory(slug='videodisc')
        response = client.get(factory.get_absolute_url())
        assert response.status_code == 200
