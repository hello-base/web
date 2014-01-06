# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models

from model_utils import FieldTracker

from components.people.models import Idol, Group

User = get_user_model()


class Show(models.Model):
    # Details
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField()

    # Run Dates (for Hello! Project shows only)
    aired_from = models.DateField(blank=True, null=True)
    aired_until = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.romanized_name


class TimeSlot(models.Model):
    show = models.ForeignKey(Show)

    # Broadcast Schedule (for Hello! Project shows only)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return '%s~%s %s' % (self.start_time, self.end_time, self.show.romanized_name)


class Episode(models.Model):
    show = models.ForeignKey(Show)
    air_date = models.DateField()

    # Continued Episodes (for episodes split into parts)
    episode = models.ForeignKey('self', blank=True, null=True, related_name='continuation')

    # Optional Information
    record_date = models.DateField(blank=True, null=True)
    romanized_name = models.CharField(blank=True, max_length=200)
    name = models.CharField(blank=True, max_length=200)
    number = models.IntegerField(blank=True, null=True)

    # Share
    video_link = models.URLField(blank=True)
    # Embed video if possible. Multiple links will be submitted by users.

    # Model Managers
    tracker = FieldTracker()

    def __unicode__(self):
        return '%s %s' % (self.air_date, self.show.romanized_name)


class Magazine(models.Model):
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    price = models.IntegerField(blank=True, null=True)
    slug = models.SlugField()
    # If prices change in the course of a magazine we may need to move this to Issue or make a Price model.

    def __unicode__(self):
        return '%s' % self.romanized_name


class Issue(models.Model):
    magazine = models.ForeignKey(Magazine, related_name='issues')  # default: issue_set
    volume_number = models.CharField(max_length=4)
    release_date = models.DateField(blank=True, null=True)
    catalog_number = models.CharField(blank=True, max_length=30)
    isbn_number = models.CharField(max_length=19)  # ?
    cover = models.ImageField(blank=True, upload_to='appearances/issues/')

    def __unicode__(self):
        return '%s #%s' % (self.magazine.romanized_name, self.volume_number)


class IssueImage(models.Model):
    issue = models.ForeignKey(Issue, related_name='gallery')
    image = models.ImageField(blank=True, upload_to='appearances/issues/')
    # Gallery will allow multiple images to be uploaded by users.

    def __unicode__(self):
        return 'Image of %s #%s' % (self.magazine.romanized_name, self.issue.volume_number)


class CardSet(models.Model):
    issue = models.ForeignKey(Issue, related_name='sets')
    romanized_name = models.CharField(max_length=200)

    # Gallery
    image = models.ImageField(blank=True, upload_to='appearances/cards/')

    def __unicode__(self):
        return '%s %s' % (self.magazine.romanized_name, self.romanized_name)


class Card(models.Model):
    issue = models.ForeignKey(Issue, related_name='cards')
    cardset = models.ForeignKey(CardSet, blank=True, null=True)
    hp_model = models.ForeignKey(Idol, blank=True, null=True, related_name='cards')
    member_of = models.ForeignKey(Group, blank=True, null=True, related_name='idol')
    group = models.ForeignKey(Group, blank=True, null=True, related_name='cards')
    number = models.IntegerField(blank=True, null=True)
    image = models.ImageField(blank=True, upload_to='appearances/cards/')

    # Non-H!P Model Information
    other_model_romanized_name = models.CharField(blank=True, max_length=200)
    other_model_name = models.CharField(blank=True, max_length=200)
    other_member_of_romanized_name = models.CharField(blank=True, max_length=200)
    other_member_of_name = models.CharField(blank=True, max_length=200)
    other_group_romanized_name = models.CharField(blank=True, max_length=200)
    other_group_name = models.CharField(blank=True, max_length=200)
    # Models must always be named, even if card features a group.
    # When the model is not a H!B idol, CharField to input name/romanized_name/group name/group romanized name.

    def __unicode__(self):
        if self.number:
            return '%s card no. %s' % (self.issue, self.number)
        if self.group or self.other_group_romanized_name:
            return '%s card feat. %s' % (self.issue, self.group_romanized_name)
        return '%s card feat. %s' % (self.issue, self.model_romanized_name)

    @property
    def group_name(self):
        return filter(None, [
            self.other_group_name,
            getattr(self.group, 'name', '')
        ])[0]

    @property
    def group_romanized_name(self):
        return filter(None, [
            self.other_group_romanized_name,
            getattr(self.group, 'romanized_name', '')
        ])[0]

    @property
    def model_name(self):
        return filter(None, [
            self.other_model_name,
            getattr(self.hp_model, 'name', '')
        ])[0]

    @property
    def model_romanized_name(self):
        return filter(None, [
            self.other_model_romanized_name,
            getattr(self.hp_model, 'romanized_name', '')
        ])[0]


class Summary(models.Model):
    body = models.TextField(blank=True)
    submitted_by = models.ForeignKey(User, blank=True, null=True, related_name='%(class)s_submissions')

    # Multiple summaries can be submitted by users.
    # Summaries can be connected to either episodes or magazine issues.
    episode = models.ForeignKey(Episode, blank=True, null=True, related_name='summaries')
    issue = models.ForeignKey(Issue, blank=True, null=True, related_name='summaries')

    # Model Managers.
    tracker = FieldTracker()

    class Meta:
        verbose_name_plural = 'summaries'

    def __unicode__(self):
        return '%s %s synopsis' % (self.episode.air_date, self.episode.romanized_name)
