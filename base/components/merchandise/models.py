# -*- coding: utf-8 -*-
from django.db import models

from django_extensions.db import fields as extensions

from components.accounts.models import ContributorMixin
from components.people.models import ParticipationMixin


class Merchandise(ContributorMixin, ParticipationMixin):
    # Shared metadata.
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    released = models.DateField(blank=True, db_index=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    # Secondary identifier.
    uuid = extensions.UUIDField(auto=True)

    class Meta:
        abstract = True


class AlternateAttributionMixin(models.Model):
    released_as = models.CharField(blank=True, max_length=200,
        help_text='Used for temporary name changes (i.e., むてん娘。).')
    romanized_released_as = models.CharField(blank=True, max_length=200,
        help_text='Used for temporary name changes (i.e., Muten Musume).')

    class Meta:
        abstract = True
