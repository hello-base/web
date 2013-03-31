from django.db import models

class Show(models.Model):
	romanized_name = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	aired_from = models.DateField(blank=True)
	aired_until = models.DateField(blank=True)
	start_time = models.DateTimeField(blank=True)
	end_time = models.DateTimeField(blank=True)
	# Aired from/until only for HelloPro shows.
	# Start/end time only for HelloPro shows (to derrive in Episodes model).


class Episode(models.Model):
	romanized_name = models.CharField(blank=True)
	name = models.CharField(blank=True)
	number = models.IntegerField(blank=True)
	air_date = models.DateField()
	record_date = models.DateField(blank=True)
	synopsis = models.TextField(blank=True)
	video_link = models.URLField(blank=True)
	show = models.ForeignKey(Show)
	# Look into smart way to derrive episode number for HelloPro shows.
	# Look into linking episode if they're continuations.
	# Multiple synopsese will be submitted by users.
	# Embed video if possible. Multiple links will be submitted by users.


class Magazine(models.Model):
	romanized_name = models.CharField(max_length=200)
	name = models.CharField(max_length=200)


class Issue(models.Model):
	magazine = models.ForeignKey(Magazine, related_name='issues') # default: issue_set
	volume_number = models.IntegerField()
	release_date = models.DateField(blank=True)
	catalog_number = models.CharField(blank=True)
	cover = models.ImageField(blank=True)
	price = models.IntegerField(blank=True)
	isbn_number = models.CharField(max_length=19) # ?
	gallery = models.ImageField(blank=True)
	# Possibly move price to Magazine model.
	# Gallery will allow multiple images to be uploaded by users.

	def all_available_cards(self):
		return self.available_cards.all()


class Set(models.Model):
	issue = models.ForeignKey(Issue, related_name='sets')
	image = models.ImageField(blank=True)


class Card(models.Model):
	issue = models.ForeignKey(Issue, related_name='available_cards')
	set = models.ForeignKey(Set, blank=True, null=True)
	model = models.ForeignKey(Idol, blank=True, related_name='models')
	image = models.ImageField(blank=True)
	# Sometimes multiple models will be featured in a card.
	# Derrive H!B idol from existing database, but group they belong to set manually.
	# When the model is not a H!B idol, CharField to input name/romanized_name/group.