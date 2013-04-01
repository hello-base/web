from django.db import models
	

class Source(models.Model):
	romanized_name = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	website_link = models.URLField(blank=True)
	# Sources include HelloShop.jp, other websites, official store, etc.
	# HelloShop.jp sections will be defined as separate sources (Egao, Special, etc).
	# Campaign goods (freebies) may also be defined as a source?


class Good(models.Model):
	romanized_name = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	price = models.IntegerField(blank=True, null=True)
	event = models.ForeignKey(Event, blank=True, null=True)
	source = models.ForeignKey(Source, blank=True, null=True)
	available_from = models.DateField(blank=True, null=True)
	available_until = models.DateField(blank=True, null=True)
	link = models.URLFeild(blank=True)
	image = models.ImageField(blank=True)
	# Look into goods that are part of an event having the same available from/until date.
	# A Good is either from a Source or from an Event, not both. Exception: HelloShop.jp Goods section.