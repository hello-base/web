from django.contrib import admin
from django.db import models

from model_utils import FieldTracker


class Event(models.Model):
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    info_link = models.URLField(blank=True, null=True)
    secondary_info_link = models.URLField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    slug = models.SlugField()

    # Model Managers
    tracker = FieldTracker()

    def __unicode__(self):
        return u'%s' % self.romanized_name


class Venue(models.Model):
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    former_names = models.CharField(max_length=200, blank=True, null=True)
    romanized_address = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField()
    # Country field only filled if outside US (maybe unnecessary).

    def __unicode__(self):
        return u'%s' % self.romanized_name

class Performance(models.Model):
    day = models.DateField()
    romanized_name = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    event = models.ForeignKey(Event, related_name='schedule')
    venue = models.ForeignKey(Venue, blank=True, null=True, related_name='performances')
    # Add 'set list' field with convoluted ordering and everything...
    
    class Meta:
        ordering = ('day', 'start_time')

    def __unicode__(self):
        if self.start_time:
            return u'%s %s at %s' % (self.day, self.event.nickname, self.start_time)
        return u'%s %s' % (self.day, self.event.nickname)


# -HACK- to quickly input data.
admin.site.register(Event)
admin.site.register(Performance)
admin.site.register(Venue)
