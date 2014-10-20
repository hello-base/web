# -*- coding: utf-8 -*-
import pytest

from base.apps.history.factories import HistoryFactory
from base.apps.history.models import History

pytestmark = pytest.mark.django_db


class TestHistories:
    def test_factory(self):
        factory = HistoryFactory()
        assert isinstance(factory, History)

    def test_deltas(self):
        history1 = HistoryFactory(sum=10)
        history2 = HistoryFactory(sum=20)
        history3 = HistoryFactory(sum=10)
        assert history1.delta == 0
        assert history2.delta == 10
        assert history3.delta == -10
