# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models

from components.accounts.models import ContributorMixin
from components.people.models import ParticipationMixin


class Event(ContributorMixin, ParticipationMixin):
    # Details.
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
    category = models.CharField(choices=CATEGORIES, max_length=16)
    has_handshake = models.BooleanField('has handshake?', default=False)
    is_fanclub = models.BooleanField('fanclub?', default=False)
    is_international = models.BooleanField('international?', default=False)
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=30)
    info_link_name = models.CharField(max_length=200, blank=True, 
        help_text='Separate multiple link names by comma (must have accompanying info link).')
    info_link = models.URLField(blank=True, null=True, 
        help_text='Seperate multiple links with comma (must have accompanying link name).')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    slug = models.SlugField()

    # Imagery.
    logo = models.ImageField(blank=True, null=True, upload_to='events/events/')
    promotional_image = models.ImageField(blank=True, null=True, upload_to='events/events/')
    stage = models.ImageField(blank=True, null=True, upload_to='events/events/')

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
    event = models.ForeignKey(Event, related_name='schedule')
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
    event = models.ForeignKey(Event, related_name='schedule')
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

class Summary(models.Model):
    body = models.TextField(blank=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='%(class)s_submissions')

    # Multiple summaries can be submitted by users.
    # Summaries can be connected to either events, performances (for MC's, etc.) or activities.
    event = models.ForeignKey(Event, blank=True, null=True, related_name='summaries')
    activity = models.ForeignKey(Activity, blank=True, null=True, related_name='summaries')
    performance = models.ForeignKey(Performance, blank=True, null=True, related_name='summaries')

    # Model Managers.
    tracker = FieldTracker()

    class Meta:
        verbose_name_plural = 'summaries'

    def __unicode__(self):
        if self.event:
            return '%s summary' % (self.event.nickname)
        if self.activity:
            return '%s %s activity summary' % (self.activity.day, self.activity.event.nickname)
        if self.performance:
            return '%s %s at %s summary' % (self.performance.day, self.performance.event.nickname, self.performance.start_time)
