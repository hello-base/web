# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import get_model

from django_extensions.db import fields as extensions

from components.accounts.models import ContributorMixin
from components.people.models import ParticipationMixin

# The below subjects are written as strings for circular import reasons.
# We'll be using get_model() instead of importing them directly.
PURCHASE_SUBJECTS = [
    'appearances.issue',           # appearances
    'music.album', 'music.single'  # merchandise.music
]


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


class Store(models.Model):
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(blank=True, max_length=200)
    url = models.URLField(blank=True)

    def __unicode__(self):
        return '%s' % (self.romanized_name)


class PurchaseLink(models.Model):
    store = models.ForeignKey(Store)
    url = models.URLField(blank=True)

    def __unicode__(self):
        return '%s' % (self.url)


# Purchase subjects.
for subject in PURCHASE_SUBJECTS:
    subject = get_model(*subject.split('.'))
    PurchaseLink.add_to_class(
        subject._meta.model_name,
        models.ForeignKey(subject, blank=True, null=True, related_name='purchase_links')
    )
