# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

from apps.people.models import Group


def total_group_count_over_time(datetime):
    # Calculates the total active groups for a given date.
    fields = {
        'tag': 'total-group-count',
        'datetime': datetime,
        'source': ContentType.objects.get(app_label='people', model='group'),
        'sum': Group.objects.active(target=datetime).count(),
    }
    return fields


def total_idol_count_over_time(datetime):
    # Calculates the total active idols for a given date.
    fields = {
        'tag': 'total-idol-count'
    }
    return fields
