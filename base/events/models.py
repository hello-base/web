from django.db import models

class Event(models.Model):
	name = models.CharField(max_length=200)
	url = models.UrlField()
	start_date = models.DateField()
	end_date = models.DateField()