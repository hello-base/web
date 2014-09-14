# -*- coding: utf-8 -*-
import pytest

from base.apps.merchandise.media.factories import (VideodiscFactory,
    VideodiscFormatFactory)
from base.apps.merchandise.media.models import Videodisc, VideodiscFormat

pytestmark = pytest.mark.django_db


class TestVideodiscs:
    def test_factory(self):
        factory = VideodiscFactory()
        assert isinstance(factory, Videodisc)

    def test_get_absolute_url(self, client):
        factory = VideodiscFactory(slug='videodisc')
        response = client.get(factory.get_absolute_url())
        assert response.status_code == 200


class TestVideodiscFormat:
    def test_factory(self):
        factory = VideodiscFormatFactory()
        assert isinstance(factory, VideodiscFormat)
        assert isinstance(factory.parent, Videodisc)
