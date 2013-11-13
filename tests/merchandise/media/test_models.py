# -*- coding: utf-8 -*-
import pytest

from components.people.factories import GroupFactory, IdolFactory
from components.merchandise.media.factories import VideodiscFactory
from components.merchandise.media.models import Videodisc


class TestVideodiscs:
    def test_factory(self):
        factory = VideodiscFactory()
        assert isinstance(factory, Videodisc)
