# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models

from model_utils import Choices

from base.apps.people.models import ParticipationMixin
from base.apps.merchandise.models import Merchandise


class Videodisc(Merchandise):
    VIDEO_TYPES = Choices(
        ('Performances', [
            (1, 'bestshot', 'Best Shot'),
            (2, 'concert', 'Concert'),
            (3, 'movie', 'Movie'),
            (4, 'musical', 'Musical'),
            (5, 'stageplay', 'Stage Play'),
            (6, 'visual', 'Visual'),
        ]),
        ('Compilations', [
            (11, 'pvcollections', 'PV Collections'),
            (12, 'tvsegments', 'Television Segments'),
        ]),
        (99, 'other', 'Other'),
    )

    kind = models.IntegerField(choices=VIDEO_TYPES, default=VIDEO_TYPES.concert)
    slug = models.SlugField(blank=True)

    def get_absolute_url(self):
        return reverse('videodisc-detail', kwargs={'slug': self.slug})


class VideodiscFormat(models.Model):
    FORMAT_TYPES = Choices((1, 'dvd', 'DVD'), (2, 'bluray', 'Blu-ray Disc'))
    parent = models.ForeignKey(Videodisc, blank=True, null=True, related_name='formats')

    # Metadata
    kind = models.IntegerField(choices=FORMAT_TYPES, default=FORMAT_TYPES.dvd)
    released = models.DateField(blank=True, db_index=True, null=True)
    catalog_number = models.CharField(blank=True, max_length=25)

    # Content
    art = models.ImageField(blank=True, null=True, upload_to='merchandise/media/videos/')
    clips = models.ManyToManyField('music.Track', blank=True, null=True, related_name='videos', through='Clip')

    class Meta:
        get_latest_by = 'released'
        ordering = ('-released',)
        verbose_name = 'format'

    def __unicode__(self):
        return u'%s' % (self.parent.romanized_name)


class Clip(ParticipationMixin):
    romanized_name = models.CharField(blank=True, max_length=200,
        help_text='This should be filled out if there is no coorresponding track or if the clip was an MC.')
    name = models.CharField(blank=True, max_length=200)
    format = models.ForeignKey(VideodiscFormat, related_name='order')
    track = models.ForeignKey('music.Track', blank=True, null=True, related_name='on_formats')
    disc = models.PositiveSmallIntegerField(default=1)
    position = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('format', 'disc', 'position')

    def __unicode__(self):
        if self.romanized_name:
            return u'%s on %s' % (self.romanized_name, self.format)
        return u'%s on %s' % (self.track, self.format)
