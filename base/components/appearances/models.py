# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from model_utils import FieldTracker

from components.people.models import Idol, Group, ParticipationMixin


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


class Episode(ParticipationMixin, models.Model):
    show = models.ForeignKey(Show)
    air_date = models.DateField()

    # Continued Episodes (for episodes split into parts)
    episode = models.ForeignKey('self', blank=True, null=True, related_name='continuation')

    # Optional Information
    is_coverage = models.BooleanField('is coverage?', default=False)
    record_date = models.DateField(blank=True, null=True)
    romanized_name = models.CharField(blank=True, max_length=200)
    name = models.CharField(blank=True, max_length=200)
    number = models.IntegerField(blank=True, null=True)

    # Share
    video_link = models.URLField(blank=True, max_length=500)

    # Model Managers
    tracker = FieldTracker()

    class Meta:
        ordering = ('show', 'air_date')

    def __unicode__(self):
        return '%s %s' % (self.air_date, self.show.romanized_name)


class Magazine(models.Model):
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    price = models.IntegerField(blank=True, null=True)
    slug = models.SlugField()

    def __unicode__(self):
        return '%s' % self.romanized_name


class Issue(ParticipationMixin, models.Model):
    magazine = models.ForeignKey(Magazine, related_name='issues')  # default: issue_set
    price = models.IntegerField(blank=True, null=True,
        help_text='If different from magazine price.')
    volume = models.CharField(blank=True, max_length=10,
        help_text='Leave blank if no volume number (but fill out month or week).')
    volume_month = models.DateField(blank=True, null=True,
        help_text='1st day of the month. Leave blank for weekly magazines.')
    volume_week = models.DateField(blank=True, null=True,
        help_text='Leave blank for monthly magazines.')
    release_date = models.DateField(blank=True, null=True)
    catalog_number = models.CharField(blank=True, max_length=30,
        help_text='Most magazines dont have this, NEOBK is just a Neowing ID.')
    isbn_number = models.CharField(max_length=20, blank=True,
        help_text='JAN number works too, its like a Japanese ISBN.')
    cover = models.ImageField(blank=True, upload_to='appearances/issues/')

    def __unicode__(self):
        if any(self.volume, self.volume_month, self.volume_week):
            return '%s Vol. %s' % (self.magazine.romanized_name, self.get_volume())
        return '%s released %s' % (self.magazine.romanized_name, self.release_date)

    def save(self, *args, **kwargs):
        if not self.pk and self.magazine.price:
            self.price = self.magazine.price
        return super(Issue, self).save(*args, **kwargs)

    def get_volume(self):
        volume_fields = [self.volume, self.volume_month, self.volume_week]
        return [field for field in volume_fields if field]


class IssueImage(models.Model):
    issue = models.ForeignKey(Issue, related_name='gallery')
    image = models.ImageField(blank=True, upload_to='appearances/issues/')
    # Gallery will allow multiple images to be uploaded by users.

    def __unicode__(self):
        return 'Image of %s' % (self.magazine.romanized_name)


class CardSet(models.Model):
    issue = models.ForeignKey(Issue, related_name='sets')
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(blank=True, max_length=200)

    # Gallery
    image = models.ImageField(blank=True, upload_to='appearances/cards/')

    def __unicode__(self):
        return '%s %s' % (self.magazine.romanized_name, self.romanized_name)


class Card(models.Model):
    issue = models.ForeignKey(Issue, related_name='cards')
    cardset = models.ForeignKey(CardSet, blank=True, null=True)
    hp_model = models.ForeignKey(Idol, blank=True, null=True, related_name='cards', verbose_name='H!P model')
    member_of = models.ForeignKey(Group, blank=True, null=True, related_name='idol')
    group = models.ForeignKey(Group, blank=True, null=True, related_name='cards')
    number = models.IntegerField(blank=True, null=True)
    image = models.ImageField(blank=True, upload_to='appearances/cards/')

    # Non-H!P Model Information
    other_model_romanized_name = models.CharField('model (romanized name)', blank=True, max_length=200)
    other_model_name = models.CharField('model (name)', blank=True, max_length=200)
    other_member_of_romanized_name = models.CharField('member of (romanized name)', blank=True, max_length=200)
    other_member_of_name = models.CharField('member of (name)', blank=True, max_length=200)
    other_group_romanized_name = models.CharField('group (romanized name)', blank=True, max_length=200)
    other_group_name = models.CharField('group (name)', blank=True, max_length=200)
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
