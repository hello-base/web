from django.db import models

class Magazine(models.Model):
	name = models.CharField(max_length=50)
	

class Issue(models.Model):
	magazine = models.ForeignKey(Magazine, related_name='issues') # default: issue_set
	
	volume_number = models.IntegerField()
	release_date = models.DateField()
	catalog_number = models.CharField()
	cover = models.ImageField(blank=True)
	price = models.IntegerField()
	isbn_number = models.CharField(max_length=19) # ?
	cards_photo = models.ImageField(blank=True)

	def all_available_cards(self):
		return self.available_cards.all()
	

class Set(models.Model):
	issue = models.ForeignKey(Issue, related_name='sets')
	set_photo = models.ImageField(blank=True)
	

class Card(models.Model):
	issue = models.ForeignKey(Issue, related_name='available_cards')
	set = models.ForeignKey(Set, blank=True, null=True)