from django.db import models
	

class Source(models.Model):
	romanized_name = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	url = models.URLField(blank=True)


class Good(models.Model):
	romanized_name = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	event = models.ForeignKey(Event, blank=True)
	source = models.ForeignKey(Source, blank=True)
	available_from = models.DateField(blank=True)
	available_until = models.DateField(blank=True)
	url = models.URLFeild(blank=True)
	image = models.ImageField(blank=True)
