from django.db import models
	

class Source(models.Model):
	name = models.CharField(max_length=200)
	url = models.UrlField(blank=True)
	
	
class Good(models.Model):
	name = models.CharField(max_length=200)
	event = models.ForeignKey(Event, blank=True)
	source = models.ForeignKey(Source, blank=True)
	available_from = models.DateField(blank=True)
	available_until = models.DateField(blank=True)
	url = models.UrlFeild(blank=True)
	image = models.ImageField(blank=True)
	