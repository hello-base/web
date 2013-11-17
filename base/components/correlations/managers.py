# -*- coding: utf-8 -*-
from datetime import date

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import smart_text

from components.people.models import Membership

FIELDS = [
    # Positive dates.
    'birthdate',            # people.Idol
    'started'               # people.Idol, people.Group, people.Membership
    'leadership_started'    # people.Membership
    'released'              # merchandise.*

    # Negative dates.
    'graduated',            # people.Idol
    'retired',              # people.Idol
    'ended',                # people.Group, people.Membership
    'leadership_ended',     # people.Membership
]


def call_attributes(instance, attribute_list):
    for attribute in attribute_list:
        if hasattr(instance, attribute):
            return (getattr(instance, attribute), attribute)
    raise AttributeError


class EventManager(models.Manager):
    def create_or_update(self, sender, instance, **kwargs):
        # Membership is a special case. Since most groups are static
        # (or non-generational), the date the group is formed is the same as
        # the date its members joined. So if those two values are equal, stop
        # the process.
        if (isinstance(sender, Membership)
            and instance.group is not None
            and instance.started == instance.group.started):
            return
        timestamp, attribute = call_attributes(instance, FIELDS)
        if timestamp is not None and timestamp != date.min:
            ctype = ContentType.objects.get_for_model(sender)
            event, created = self.get_or_create(
                content_type=ctype,
                object_id=smart_text(instance._get_pk_val()),
                defaults={
                    'timestamp': timestamp,
                    'date_field': attribute,
                    'julian': timestamp.timetuple().tm_yday,
                    'year': timestamp.year,
                    'month': timestamp.month,
                    'day': timestamp.day,
                }
            )
