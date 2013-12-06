# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import FIELDS, MODELS
from .managers import CorrelationManager


class Correlation(models.Model):
    """
    Correlations represent activities that occur to any items that have dates.
    Each activity is referred to via a generic relation. Objects can answer
    "What is coming up?" questions as well as ones for "What happened on this
    day in Hello! Project history?"

    """
    # Model Managers.
    objects = CorrelationManager()

    # Correlation Object.
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField('object ID')
    content_object = generic.GenericForeignKey()

    # Correlation Details.
    timestamp = models.DateField(blank=True)
    identifier = models.CharField(max_length=25)
    date_field = models.CharField(max_length=25)
    description = models.TextField(blank=True)

    # Date Details.
    julian = models.PositiveSmallIntegerField('julian date', max_length=3,
        help_text='The day of the year (1 to 365).')
    year = models.PositiveSmallIntegerField(max_length=4)
    month = models.PositiveSmallIntegerField(max_length=2)
    day = models.PositiveSmallIntegerField(max_length=2)

    class Meta:
        get_latest_by = 'timestamp'
        ordering = ('-timestamp',)

    def __unicode__(self):
        return 'Correlation for %s [%s]' % (self.content_object, self.timestamp)


@receiver(post_save)
def record_correlation(sender, instance, **kwargs):
    # Being a signal without a sender, we need to make sure models are the ones
    # we're looking for before we continue.
    if not type(instance) in MODELS:
        return

    for field in FIELDS:
        try:
            timestamp = getattr(instance, field)
        except AttributeError as e:
            print(e)  # ew...
            continue
        else:
            instance.sender = sender
            Correlation.objects.update_or_create(instance, timestamp, field)
