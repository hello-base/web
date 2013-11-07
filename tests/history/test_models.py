# -*- coding: utf-8 -*-
import pytest

from components.history.factories import HistoryFactory
from components.history.models import History

pytestmark = pytest.mark.django_db


class TestHistories:
    def test_factory(self):
        factory = HistoryFactory()
        assert isinstance(factory, History)
