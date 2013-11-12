import datetime
import pytest

from django.contrib.contenttypes.models import ContentType

from components.history.metrics import (total_group_count_over_time,
    total_idol_count_over_time)
from components.people.factories import GroupFactory

pytestmark = pytest.mark.django_db


def test_total_group_count_over_time():
    target = datetime.date.today()
    [GroupFactory() for i in xrange(10)]
    assert total_group_count_over_time(target) == {
        'tag': 'total-group-count',
        'datetime': target,
        'source': ContentType.objects.get(app_label='people', model='group'),
        'sum': 10,
    }


def test_total_idol_count_over_time():
    target = datetime.date.today()
    assert total_idol_count_over_time(target) == {
        'tag': 'total-idol-count'
    }
