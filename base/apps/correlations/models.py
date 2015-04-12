# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from model_utils import Choices

from .managers import CorrelationManager


class Correlation(models.Model):
    """
    Correlations represent activities that occur to any items that have dates.
    Each activity is referred to via a generic relation. Objects can answer
    "What is coming up?" questions as well as ones for "What happened on this
    day in Hello! Project history?"

    """
    CLASSIFICATION = Choices(
        (0, 'major', 'Major'),
        (1, 'normal', 'Normal'),
        (2, 'minor', 'Minor'),
    )

    # Model Managers.
    objects = CorrelationManager()

    # Correlation Object.
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField('object ID')
    content_object = GenericForeignKey()

    # Correlation Details.
    timestamp = models.DateField(blank=True)
    identifier = models.CharField(max_length=25)
    date_field = models.CharField(max_length=25)
    description = models.TextField(blank=True)
    classification = models.IntegerField(choices=CLASSIFICATION, default=CLASSIFICATION.normal)

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
        return '%s [%s:%s]' % (self.timestamp, self.content_type_id, self.object_id)

    def related_label(self):
        return '%s [%s %s]' % (self.content_object, self.date_field, self.timestamp)

    def get_include_template(self):
        return 'correlations/partials/happenings_list_%ss.html' % (self.identifier)

    def actor(self):
        return self.content_object.idol if self.identifier == 'membership' else self.content_object

    @staticmethod
    def autocomplete_search_fields():
        return ('id__exact',)


@receiver(post_save)
def record_correlation(sender, instance, **kwargs):
    from .constants import FIELDS, MODELS

    # Being a signal without a sender, we need to make sure models are the ones
    # we're looking for before we continue.
    if not type(instance) in MODELS:
        return

    for field in FIELDS:
        try:
            instance.sender = sender
            timestamp = getattr(instance, field)
            Correlation.objects.update_or_create(instance, timestamp, field)
        except AttributeError as e:
            print(e)  # ew...
            continue
