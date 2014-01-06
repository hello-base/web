# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from components.events.models import Event, Performance
from components.merchandise.music.models import Album, Single
from components.people.models import Idol, Group

SUBJECTS = [
    Idol, Group,        # people
    Album, Single,      # merchandise.music
    Event, Performance  # events
]


class Fact(models.Model):
    body = models.TextField()

    def __unicode__(self):
        return '%s: %s...' % (self.parent.romanized_name, self.body[:40])

    @property
    def parent(self):
        return filter(None, [getattr(self, subject._meta.model_name) for subject in SUBJECTS])[0]


# Subjects.
# In an everlasting effort to not repeat thyself, we create the subject
# foreign keys dynamically. In order to do that, we have to do it outside
# of the initial model specification.
for subject in SUBJECTS:
    Fact.add_to_class(
        subject._meta.model_name,
        models.ForeignKey(subject, blank=True, null=True, related_name='%(class)ss')
    )
