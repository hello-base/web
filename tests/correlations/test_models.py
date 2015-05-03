# -*- coding: utf-8 -*-
import datetime
import pytest

from apps.correlations.models import Correlation
from apps.people.factories import GroupFactory, IdolFactory

pytestmark = pytest.mark.django_db


class TestCorrelations:
    def test_basic_correlation(self):
        group = GroupFactory(started=datetime.date(2013, 1, 1))
        assert Correlation.objects.count() == 1

        correlation = Correlation.objects.all()[0]
        assert correlation.timestamp == group.started
        assert correlation.identifier == 'group'
        assert correlation.date_field == 'started'
        assert correlation.julian == 1
        assert correlation.year == 2013
        assert correlation.month == 1
        assert correlation.day == 1

        # Take the same group and change the started date, this should update
        # the correlation, rather than create a new one.
        group.started = datetime.date(2013, 1, 2)
        group.save()
        assert Correlation.objects.count() == 1

        correlation = Correlation.objects.all()[0]
        assert correlation.timestamp == group.started
        assert correlation.julian == 2
        assert correlation.year == 2013
        assert correlation.month == 1
        assert correlation.day == 2

    def test_multiple_correlations(self):
        IdolFactory(birthdate=datetime.date(1983, 4, 2), started=datetime.date(2013, 1, 1))
        assert Correlation.objects.count() == 2
