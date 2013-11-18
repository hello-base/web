# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from model_utils.managers import PassThroughManager

from .managers import CorrelationQuerySet
from .utils import call_attributes


class Correlation(models.Model):
    """
    Correlations represent activities that occur to any items that have dates.
    Each activity is referred to via a generic relation. Objects can answer
    "What is coming up?" questions as well as ones for "What happened on this
    day in Hello! Project history?"

    """
    # Model Managers.
    objects = PassThroughManager.for_queryset_class(CorrelationQuerySet)()

    # Correlation Object.
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField('object ID')
    content_object = generic.GenericForeignKey()

    # Correlation Details.
    timestamp = models.DateField(blank=True)
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
        ordering = ('-timestamp',)

    def __unicode__(self):
        return 'Correlation for %s [%s]' % (self.content_object, self.timestamp)


FIELDS = [
    # Positive dates.
    'birthdate',            # people.Idol
    'started',              # people.Idol, people.Group, people.Membership
    'leadership_started',   # people.Membership
    'released',             # merchandise.*

    # Negative dates.
    'graduated',            # people.Idol
    'retired',              # people.Idol
    'ended',                # people.Group, people.Membership
    'leadership_ended',     # people.Membership
]


@receiver(post_save)
def record_correlation(sender, instance, **kwargs):
    # Being a signal without a sender, we need to make sure models are the ones
    # we're looking for before we continue.
    model_name = instance._meta.model_name
    MODELS = ['album', 'single', 'group', 'idol', 'membership']
    if not model_name in MODELS:
        return

    timestamp, attribute = call_attributes(instance, FIELDS)
    # Membership is a special case. Since most groups are static
    # (or non-generational), the date the group is formed is the same as
    # the date its members joined. So if those two values are equal, stop
    # the process.
    if not timestamp or (model_name == 'membership'
        and instance.started == instance.group.started):
        return

    ctype = ContentType.objects.get_for_model(sender)
    defaults = {
        'timestamp': timestamp,
        'julian': timestamp.timetuple().tm_yday,
        'year': timestamp.year,
        'month': timestamp.month,
        'day': timestamp.day,
    }
    correlation, created = Correlation.objects.get_or_create(
        content_type=ctype,
        object_id=instance._get_pk_val(),
        identifier=model_name,
        date_field=attribute,
        defaults=defaults
    )
    for key, value in defaults.iteritems():
        setattr(correlation, key, value)
    correlation.save()
