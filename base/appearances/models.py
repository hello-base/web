from django.db import models

class Show(models.Model):
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    aired_from = models.DateField(blank=True, null=True)
    aired_until = models.DateField(blank=True, null=True)
    # Aired from/until is only for HelloPro shows.
    
    def __unicode__(self):
        return u'%s' self.romanized_name


class TimeSlot(models.Model):
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    show = models.ForeignKey(Show)
    # TimeSlot is only for HelloPro shows.
    
    def __unicode__(self):
        return u'%s~%s %s' % (self.start_time, self.end_time, self.show.romanized_name)


class Episode(models.Model):
    romanized_name = models.CharField(blank=True)
    name = models.CharField(blank=True)
    number = models.IntegerField(blank=True, null=True)
    air_date = models.DateField()
    record_date = models.DateField(blank=True, null=True)
    video_link = models.URLField(blank=True)
    show = models.ForeignKey(Show)
    episode = models.ForeignKey('self', blank=True, null=True, related_name='continuation')
    # Continuation links episodes that are continuations of each other (i.e. Part One, Part Two).
    # Embed video if possible. Multiple links will be submitted by users.
    
    def __unicode__(self):
        return u'%s %s' % (self.air_date, self.show.romanized_name)


class Synopsis(models.Model):
    body = models.TextField(blank=True)
    episode = models.ForeignKey(Episode)
    # Multiple synopsese will be submitted by users.
    
    def __unicode__(self):
        return u'%s %s synopsis' % (self.episode.air_date, self.episode.romanized_name)
    # Missing a 'submitted by' type field to identify the synopsis?


class Magazine(models.Model):
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    price = models.IntegerField(blank=True, null=True)
    # If prices change in the course of a magazine we may need to move this to Issue or make a Price model.
    
    def __unicode__(self):
        return u'%s' self.romanized_name


class Issue(models.Model):
    magazine = models.ForeignKey(Magazine, related_name='issues') # default: issue_set
    volume_number = models.IntegerField()
    release_date = models.DateField(blank=True, null=True)
    catalog_number = models.CharField(blank=True)
    cover = models.ImageField(blank=True)
    isbn_number = models.CharField(max_length=19) # ?
    
    def __unicode__(self):
        return u'%s #%s' % (self.magazine.romanized_name, self.issue.volume_number)


class IssueImage(models.Model):
    image = models.ImageField(blank=True)
    issue = models.ForeignKey(Issue, related_name='gallery')
    # Gallery will allow multiple images to be uploaded by users.
    
    def __unicode__(self):
        return u'Image of %s #%s' % (self.magazine.romanized_name, self.issue.volume_number)


class CardSet(models.Model):
    romanized_name = models.CharField(max_length=200)
    issue = models.ForeignKey(Issue, related_name='sets')
    image = models.ImageField(blank=True)
    
    def __unicode__(self):
        return u'%s %s' % (self.magazine.romanized_name, self.romanized_name)


class Card(models.Model):
    issue = models.ForeignKey(Issue, related_name='cards')
    cardset = models.ForeignKey(CardSet, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    model = models.ForeignKey(Idol, related_name='cards')
    image = models.ImageField(blank=True)
    # Sometimes multiple models will be featured in a card.
    # Derrive H!B idol from existing database, but group they belong to set manually.
    # When the model is not a H!B idol, CharField to input name/romanized_name/group name/group romanized name.
    
    def __unicode__(self):
        if self.number:
            return u'%s #%s card no. %s' % (self.magazine.romanized_name, self.issue.volume_number, self.number)
        return u'%s #%s card feat. %s' % (self.magazine.romanized_name, self.issue.volume_number, self.model.romanized_name)
