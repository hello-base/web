# -*- coding: utf-8 -*-
from datetime import date

from django.contrib.contenttypes.models import ContentType
from django.db import models


class CorrelationManager(models.Manager):
    def update_or_create(self, instance, timestamp, attribute):
        ctype = ContentType.objects.get_for_model(instance.sender)
        defaults = {
            'timestamp': timestamp,
            'julian': timestamp.timetuple().tm_yday,
            'year': timestamp.year,
            'month': timestamp.month,
            'day': timestamp.day,
        }
        correlation, created = self.get_or_create(
            content_type=ctype,
            object_id=instance._get_pk_val(),
            identifier=instance._meta.model_name,
            date_field=attribute,
            defaults=defaults
        )
        for key, value in defaults.iteritems():
            setattr(correlation, key, value)
        correlation.save()
        return

    def get_query_set(self):
        qs = super(CorrelationManager, self).get_query_set()
        return qs #.prefetch_related('content_object')

    def today(self):
        qs = self.get_query_set()
        return qs.filter(julian=date.today().timetuple().tm_yday)
