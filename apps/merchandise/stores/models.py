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

    def __unicode__(self):
        return '%s' % (self.romanized_name)


class PurchaseLink(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    url = models.URLField(blank=True)

    def __unicode__(self):
        return '%s' % (self.url)


# Purchase subjects.
for subject in PURCHASE_SUBJECTS:
    PurchaseLink.add_to_class(
        subject._meta.model_name,
        models.ForeignKey(subject, on_delete=models.CASCADE, blank=True, null=True, related_name='purchase_links')
    )
