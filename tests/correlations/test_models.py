# -*- coding: utf-8 -*-
import datetime
import pytest
import pytz

from django.contrib.contenttypes.models import ContentType

from components.correlations.factories import CorrelationFactory
from components.correlations.models import Correlation
from components.people.factories import GroupFactory, MembershipFactory

pytestmark = pytest.mark.django_db


class TestCorrelations:
    def test_factory(self):
        group = GroupFactory(started=datetime.datetime(2013, 1, 1))
        factory = CorrelationFactory(content_object=group)
        assert isinstance(factory, Correlation)

    def test_basic_correlation(self):
        group = GroupFactory(started=datetime.datetime(2013, 1, 1))
        assert Correlation.objects.count() > 0

        correlation = Correlation.objects.all()[0]
        assert correlation.timestamp == group.started.replace(tzinfo=pytz.UTC)
        assert correlation.identifier == 'group'
        assert correlation.date_field == 'started'
        assert correlation.julian == 1
        assert correlation.year == 2013
        assert correlation.month == 1
        assert correlation.day == 1

    def test_membership_exception(self):
        group = GroupFactory(started=datetime.datetime(2013, 1, 1))
        membership = MembershipFactory(group=group, started=group.started)
        content_type = ContentType.objects.get(app_label='people', model='membership')

        with pytest.raises(Correlation.DoesNotExist):
            Correlation.objects.get(content_type=content_type)
