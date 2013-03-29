from django.db import models


class Event(models.Model):
	name = models.CharField(max_length=200)
	url = models.UrlField()
	start_date = models.DateField()
	end_date = models.DateField()
	

class Source(models.Model):
	name = models.CharField(max_length=200)
	url = models.UrlField(blank=True)

	
class Good(models.Model):
	name = models.CharField(max_length=200)
	event = models.ForeignKey(Event)
	source = models.ForeignKey(Source)
	available_from = models.DateField(blank=True)
	available_until = models.DateField(blank=True)
	