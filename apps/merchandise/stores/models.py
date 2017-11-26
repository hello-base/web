# -*- coding: utf-8 -*-
from django.db import models

from apps.appearances.models import Issue
from apps.merchandise.music.models import Album, Single

PURCHASE_SUBJECTS = [
    Issue,         # appearances
    Album, Single  # merchandise.music
]


class Store(models.Model):
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(blank=True, max_length=200)
    url = models.URLField(blank=True)

    def __str__(self):
        return '%s' % (self.romanized_name)


class PurchaseLink(models.Model):
    store = models.ForeignKey(Store)
    url = models.URLField(blank=True)

    def __str__(self):
        return '%s' % (self.url)


# Purchase subjects.
for subject in PURCHASE_SUBJECTS:
    PurchaseLink.add_to_class(
        subject._meta.model_name,
        models.ForeignKey(subject, blank=True, null=True, related_name='purchase_links')
    )
