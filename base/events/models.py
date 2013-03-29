from django.db import models

class Event(models.Model):
	romanized_name = models.CharField(max_length=200)
	name = models.CharField(max_lenth=200)
	url = models.URLField(blank=True)
	start_date = models.DateField(blank=True)
	end_date = models.DateField(blank=True)
	performances = models.ForeignKey(Performance)


class Performance(models.Model):
	day = models.DateField()
	start_time = models.TimeField(blank=True)
	end_time = models.TimeField(blank=True)
	venues = models.ForeignKey(Venue, blank=True)


class Venue(models.Model):
	romanized_name = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	location = models.CharField(max_length=200)
	country = models.CharField(max_length=200, blank=True)

