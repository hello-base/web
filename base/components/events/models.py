from django.db import models

from model_utils import FieldTracker

from components.accounts.models import ContributorMixin
from components.people.models import ParticipationMixin


class Event(ContributorMixin, ParticipationMixin):
    # Model Managers.
    tracker = FieldTracker()

    # Details.
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    info_link = models.URLField(blank=True, null=True)
    secondary_info_link = models.URLField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    slug = models.SlugField()

    # Imagery.
    logo = models.ImageField(blank=True, null=True, upload_to='events/events/')
    poster = models.ImageField(blank=True, null=True, upload_to='events/events/')
    stage = models.ImageField(blank=True, null=True, upload_to='events/events/')

    def __unicode__(self):
        return u'%s' % (self.romanized_name)

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'slug': self.slug})

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains', 'romanized_name__icontains')


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
