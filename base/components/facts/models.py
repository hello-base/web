# -*- coding: utf-8 -*-
from django.db import models

from components.events.models import Event, Performance
from components.merchandise.music.models import Album, Single
from components.people.models import Idol, Group


class Fact(models.Model):
    body = models.TextField()

    # Subjects.
    album = models.ForeignKey(Album, blank=True, null=True, related_name='%(class)ss')
    group = models.ForeignKey(Group, blank=True, null=True, related_name='%(class)ss')
    idol = models.ForeignKey(Idol, blank=True, null=True, related_name='%(class)ss')
    single = models.ForeignKey(Single, blank=True, null=True, related_name='%(class)ss')
    event = models.ForeignKey(Event, blank=True, null=True, related_name='%(class)ss')
    performance = models.ForeignKey(Performance, blank=True, null=True, related_name='%(class)ss')

    def __unicode__(self):
        return u'%s: %s...' % (self.parent.romanized_name, self.body[:40])

    @property
    def parent(self):
        return filter(None, [
            self.idol, self.group, self.album, self.single, self.event, self.performance]
        )[0]
