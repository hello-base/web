# -*- coding: utf-8 -*-
from django.db import models

from components.people.models import Idol, Group


class Fact(models.Model):
    idol = models.ForeignKey(Idol, blank=True, null=True, related_name='facts')
    group = models.ForeignKey(Group, blank=True, null=True, related_name='facts')
    body = models.TextField()

    def __unicode__(self):
        return u'%s: %s...' % (self.parent.romanized_name, self.body[:40])

    @property
    def parent(self):
        return filter(None, [self.idol, self.group])[0]
