# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save


class Event(models.Model):
    # Event Object.
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField('object ID')
    content_object = generic.GenericForeignKey()

    # Event details.
    timestamp = models.DateTimeField(blank=True)
    date_field = models.CharField(max_length=20)
    descrption = models.TextField(blank=True)

    # Date details.
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
