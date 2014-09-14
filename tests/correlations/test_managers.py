# -*- coding: utf-8 -*-
import datetime
import pytest

from base.apps.correlations.models import Correlation
from base.apps.merchandise.music.factories import SingleFactory

pytestmark = pytest.mark.django_db


class TestCorrelations:
    def test_today(self):
        [SingleFactory(released=datetime.date.today()) for i in xrange(5)]
        [SingleFactory(released=datetime.date.today() - datetime.timedelta(days=1)) for i in xrange(5)]
        assert len(Correlation.objects.today()) == 5
