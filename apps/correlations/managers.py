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
        for key, value in defaults.items():
            setattr(correlation, key, value)
        correlation.save()
        return

    def get_queryset(self):
        qs = super(CorrelationManager, self).get_queryset()
        return qs

    def today(self):
        today = date.today()
        qs = self.get_queryset()
        return qs.filter(month=today.month, day=today.day)
