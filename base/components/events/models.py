from django.db import models

from model_utils import ModelTracker


class Event(models.Model):
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nickname = models.CharField(blank=True, max_length=30)
    info_link = models.URLField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    # Model Managers
    tracker = ModelTracker()

    def __unicode__(self):
        return u'%s' % self.romanized_name


class Performance(models.Model):
    day = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    event = models.ForeignKey(Event, related_name='schedule')

    def __unicode__(self):
        if self.start_time:
            return u'%s %s at %s' % (self.day, self.event.nickname, self.start_time)
        return u'%s %s' % (self.day, self.event.nickname)


class Venue(models.Model):
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    country = models.CharField(max_length=200, blank=True)
    performance = models.ForeignKey(Performance)
    # Country field only filled if outside US (maybe unnecessary).

    def __unicode__(self):
        return u'%s' % self.romanized_day
