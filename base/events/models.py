from django.db import models

class Event(models.Model):
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_lenth=200)
    info_link = models.URLField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)


class Performance(models.Model):
    day = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    event = models.ForeignKey(Event, related_name='schedule')


class Venue(models.Model):
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    country = models.CharField(max_length=200, blank=True)
    performance = models.ForeignKey(Performance)
    # Country field only filled if outside US (maybe unnecessary).
