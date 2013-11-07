# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

from components.people.models import Group

from .models import History


def total_group_count_over_time(datetime):
    # Calculates the total active groups for a given date.
    fields = {
        'tag': 'total-group-count'
        'source': ContentType.objects.get(app_label='people', model='group')
        'sum': Group.objects.active(target=datetime).count()
    }


def total_idol_count_over_time(datetime):
    # Calculates the total active idols for a given date.
    fields = {
        'tag': 'total-idol-count'
    }
