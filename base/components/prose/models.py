# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from model_utils import FieldTracker

from components.appearances.models import Episode, Issue
from components.events.models import Activity, Event
from components.merchandise.music.models import Album, Single
from components.people.models import Idol, Group

FACT_SUBJECTS = [
    Idol, Group,        # people
    Album, Single,      # merchandise.music
    Activity, Event     # events
]
SUMMARY_SUBJECTS = [
    Activity, Event,    # events
    Episode, Issue      # appearances
]


class Fact(models.Model):
    body = models.TextField()

    # Model Managers.
    tracker = FieldTracker()

    def __unicode__(self):
        return '%s: %s...' % (self.parent.romanized_name, self.body[:40])

    @property
    def parent(self):
        return filter(None, [getattr(self, subject._meta.model_name) for subject in FACT_SUBJECTS])[0]


# Fact subjects.
for subject in FACT_SUBJECTS:
    Fact.add_to_class(
        subject._meta.model_name,
        models.ForeignKey(subject, blank=True, null=True, related_name='%(class)ss')
    )


class Summary(models.Model):
    body = models.TextField(blank=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='%(class)s_submissions')

    # Model Managers.
    tracker = FieldTracker()

    class Meta:
        verbose_name_plural = 'summaries'

    def __unicode__(self):
        return '%s summary' % (self.parent)

    @property
    def parent(self):
        return filter(None, [getattr(self, subject._meta.model_name) for subject in SUMMARY_SUBJECTS])[0]


# Summary subjects.
# Multiple summaries can be submitted by users.
# Summaries can be connected to either episodes, magazine issues, events,
# performances (for MC's, etc.) or activities.
for subject in SUMMARY_SUBJECTS:
    Summary.add_to_class(
        subject._meta.model_name,
        models.ForeignKey(subject, blank=True, null=True, related_name='summaries')
    )
