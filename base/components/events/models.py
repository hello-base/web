# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models

from model_utils import Choices

from components.accounts.models import ContributorMixin
from components.people.models import ParticipationMixin


class Event(ContributorMixin, ParticipationMixin):
    CATEGORIES = Choices(
        ('birthday', 'Birthday'),
        ('bustour', 'Bus Tour'),
        ('concert', 'Concert'),
        ('convention', 'Convention'),
        ('dinnershow', 'Dinner Show'),
        ('general', 'General'),
        ('hawaii', 'Hawaii'),
        ('live', 'Live'),
        ('release', 'Release'),
        ('promotional', 'Promotional'),
        ('other', 'Other'),
    )

    # Details.
    category = models.CharField(choices=CATEGORIES, default=CATEGORIES.general, max_length=16)
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=30)
    slug = models.SlugField()

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    info_link_name = models.CharField(max_length=200, blank=True,
        help_text='Separate multiple link names by comma (must have accompanying info link).')
    info_link = models.URLField(blank=True, max_length=500, 
        help_text='Seperate multiple links with comma (must have accompanying link name).')

    # Imagery.
    logo = models.ImageField(blank=True, null=True, upload_to='events/events/')
    promotional_image = models.ImageField(blank=True, null=True, upload_to='events/events/')
    stage = models.ImageField(blank=True, null=True, upload_to='events/events/')

    # Booleans.
    has_handshake = models.BooleanField('has handshake?', default=False)
    is_fanclub = models.BooleanField('fanclub?', default=False)
    is_international = models.BooleanField('international?', default=False)

    class Meta:
        get_latest_by = 'start_date'

    def __unicode__(self):
        return u'%s' % (self.romanized_name)

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'slug': self.slug})

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains', 'romanized_name__icontains')


class Activity(ContributorMixin):
    day = models.DateField()
    romanized_name = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, blank=True)
    start_time = models.TimeField(blank=True, null=True)
    description = models.TextField(blank=True,
        help_text='If multiple activities took place on the same day/event, it can be specified here.')
    event = models.ForeignKey(Event, related_name='activity_schedule')
    venue = models.ForeignKey('Venue', blank=True, null=True, related_name='activities')
    venue_known_as = models.CharField(max_length=200, blank=True,
        help_text='Did the venue go by another name at the time of this activity?')

    class Meta:
        get_latest_by = 'day'
        ordering = ('day', 'start_time')

    def __unicode__(self):
        if self.romanized_name:
            return u'%s %s: %s' % (self.day, self.event.nickname, self.romanized_name)
        return u'%s %s' % (self.day, self.event.nickname)


class Performance(ContributorMixin):
    day = models.DateField()
    romanized_name = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, blank=True)
    start_time = models.TimeField(blank=True, null=True)
    event = models.ForeignKey(Event, related_name='performance_schedule')
    venue = models.ForeignKey('Venue', blank=True, null=True, related_name='performances')
    venue_known_as = models.CharField(max_length=200, blank=True,
        help_text='Did the venue go by another name at the time of this performance?')
    # Add 'set list' field with convoluted ordering and everything...

    class Meta:
        get_latest_by = 'day'
        ordering = ('day', 'start_time')

    def __unicode__(self):
        if self.start_time:
            return u'%s %s at %s' % (self.day, self.event.nickname, self.start_time)
        return u'%s %s' % (self.day, self.event.nickname)


class Venue(ContributorMixin):
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    other_names = models.CharField(max_length=200, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    url = models.URLField('URL', blank=True)
    slug = models.SlugField()

    # Location.
    romanized_address = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)  # Only filled if outside of Japan (maybe unnecessary).

    # Imagery.
    photo = models.ImageField(blank=True, null=True, upload_to='events/venues/')

    def __unicode__(self):
        return u'%s' % (self.romanized_name)

    def get_absolute_url(self):
        return reverse('venue-detail', kwargs={'slug': self.slug})

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains', 'romanized_name__icontains')
