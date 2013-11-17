# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import smart_text

from .utils import call_attributes


class Event(models.Model):
    """
    Events represent activities that occur to any items that have dates. Each
    activity is referred to via a generic relation. Event objects can answer
    "What is coming up?" questions as well as ones for "What happened on this
    day in Hello! Project history?"

    """
    # Model Managers.
    objects = EventManager()

    # Event Object.
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField('object ID')
    content_object = generic.GenericForeignKey()

    # Event Details.
    timestamp = models.DateTimeField(blank=True)
    identifier = models.CharField(max_length=25)
    date_field = models.CharField(max_length=25)
    descrption = models.TextField(blank=True)

    # Date Details.
    julian = models.PositiveSmallIntegerField(max_length=3)
    year = models.PositiveSmallIntegerField(max_length=4)
    month = models.PositiveSmallIntegerField(max_length=2)
    day = models.PositiveSmallIntegerField(max_length=2)

    class Meta:
        get_latest_by = 'timestamp'
        ordering = ('-timestamp')
        unique_together = ('content_type', 'object_id')

    def __unicode__(self):
        return 'Event for %s' % (self.content_object)


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

@receiver(post_save)
def record_event(sender, instance, **kwargs):
    # Being a signal without a sender, we need to make sure models are the ones
    # we're looking for before we continue.
    MODELS = ['album', 'single', 'group', 'idol', 'membership']
    if not instance._meta.model_name in MODELS:
        return

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
                'identifier': instance._meta.model_name,
                'date_field': attribute,
                'julian': timestamp.timetuple().tm_yday,
                'year': timestamp.year,
                'month': timestamp.month,
                'day': timestamp.day,
            }
        )
