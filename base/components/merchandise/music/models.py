from datetime import date
from itertools import chain

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils.functional import cached_property

from imagekit.models import ImageSpecField
from model_utils import Choices
from model_utils.models import TimeStampedModel
from ohashi.constants import OTHER
from ohashi.db import models

from components.people.models import ParticipationMixin

from ..models import Merchandise
# from .managers import (AlbumManager, EditionManager, SingleManager,
#     TrackOrderManager, VideoTrackOrderManager)


class Label(models.Model):
    name = models.CharField()
    slug = models.SlugField()

    def __unicode__(self):
        return u'%s' % self.name


class Base(Merchandise):
    # Music-specific shared metadata.
    number = models.CharField(blank=True)
    label = models.ForeignKey(Label, blank=True, null=True, related_name='%(class)ss')
    slug = models.SlugField(blank=True)

    class Meta:
        abstract = True
        get_latest_by = 'released'
        ordering = ('-released',)

    def __unicode__(self):
        return u'%s' % (self.romanized_name)

    @property
    def identifier(self):
        return self._meta.module_name

    @cached_property
    def participants(self):
        return list(chain(self.participating_idols.all(), self.participating_groups.all()))


class Album(Base):
    is_compilation = models.BooleanField('compilation?', default=False)

    def get_absolute_url(self):
        return reverse('album-detail', kwargs={'slug': self.slug})


class Single(Base):
    is_indie = models.BooleanField('indie single?', default=False)
    has_8cm = models.BooleanField('8cm version?', default=False)
    has_lp = models.BooleanField('LP version?', default=False)
    has_cassette = models.BooleanField('cassette version?', default=False)

    def get_absolute_url(self):
        return reverse('single-detail', kwargs={'slug': self.slug})


class Edition(models.Model):
    EDITIONS = Choices(
        (1, 'regular', 'Regular'),
        (2, 'limited', 'Limited'),
        (3, 'singlev', 'Single V'),
        (4, 'eventv', 'Event V'),
        (11, 'commemorative', 'Commemorative'),
        (12, 'digital', 'Digital'),
        (99, 'other', 'Other'),
    )

    album = models.ForeignKey(Album, blank=True, null=True, related_name='editions')
    single = models.ForeignKey(Single, blank=True, null=True, related_name='editions')

    # Metadata
    romanized_name = models.CharField(blank=True)
    name = models.CharField(blank=True)
    kind = models.IntegerField(choices=EDITIONS, db_index=True, default=EDITIONS.regular)
    released = models.DateField(blank=True, db_index=True, null=True)
    catalog_number = models.CharField(blank=True)
    price = models.IntegerField(blank=True, null=True)

    # Contents
    art = models.ImageField(blank=True, null=True, upload_to='merchandise/music/editions/')
    tracks = models.ManyToManyField('Track', blank=True, null=True, related_name='editions', through='TrackOrder')
    videos = models.ManyToManyField('Video', blank=True, null=True, related_name='editions', through='VideoTrackOrder')

    class Meta:
        get_latest_by = 'released'
        ordering = ('kind', 'romanized_name')

    def __unicode__(self):
        if self.parent:
            return u'%s [%s]' % (self.parent.romanized_name, self.romanized_name)
        return u'%s' % (self.name)

    def get_absolute_url(self):
        return self.parent.get_absolute_url()

    def save(self, *args, **kwargs):
        if not self.romanized_name:
            self.romanized_name = self.get_kind_display()
        if self.kind in [self.EDITIONS.regular, self.EDITIONS.digital]:
            if self.released:
                self.parent.released = self.released
                self.parent.save()
            elif not self.released:
                self.released = date.min
        elif not self.released:
            self.released = self.parent.released
        return super(Edition, self).save(*args, **kwargs)

    def _get_regular_edition(self):
        try:
            kwargs = {self.parent.identifier: self.parent, 'kind': self.EDITIONS.regular}
            edition = self._default_manager.filter(**kwargs)[0]
        except IndexError:
            edition = self._default_manager.none()
        return edition

    def _render_release_date(self):
        return self._get_regular_edition().released

    def _render_tracklist(self):
        if self.kind != self.EDITIONS.regular and not self.order.exists():
            return self._get_regular_edition().order.select_related('track')
        return self.order.select_related('track')

    def participants(self):
        return self.parent.participants()

    @property
    def parent(self):
        return filter(None, [self.album, self.single])[0]

    @cached_property
    def tracklist(self):
        if self.kind in [self.EDITIONS.eventv, self.EDITIONS.singlev]:
            return self.order.none()
        tracklist = self._render_tracklist()
        return tracklist


class Track(ParticipationMixin):
    # Metadata.
    romanized_name = models.CharField()
    name = models.CharField(blank=True)

    # Alternate Versions.
    original_track = models.ForeignKey('self', blank=True, null=True, related_name='parent',
        help_text='If this track is a cover or alternate, choose the original track it\'s based off of.')
    is_cover = models.BooleanField('cover?', default=False)
    is_alternate = models.BooleanField('alternate?', default=False)
    romanized_name_alternate = models.CharField('alternate name (romanized)', blank=True)
    name_alternate = models.CharField('alternate name', blank=True)

    # Staff.
    arrangers = models.ManyToManyField('people.Staff', blank=True, null=True, related_name='arranged')
    composers = models.ManyToManyField('people.Staff', blank=True, null=True, related_name='composed')
    lyricists = models.ManyToManyField('people.Staff', blank=True, null=True, related_name='wrote')

    def __unicode__(self):
        if self.is_alternate:
            return u'%s [%s]' % (self.romanized_name, self.romanized_name_alternate)
        if self.is_cover and not self.is_alternate:
            return u'%s [Cover]' % (self.romanized_name)
        return u'%s' % (self.romanized_name)

    def get_absolute_url(self):
        return reverse('track-detail', kwargs={'pk': self.pk})

    def participants(self):
        return list(chain(self.idols.all(), self.groups.all()))

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains', 'romanized_name__icontains')


class TrackOrder(models.Model):
    edition = models.ForeignKey(Edition, related_name='order')
    track = models.ForeignKey(Track, related_name='appears_on')
    position = models.PositiveSmallIntegerField()

    # A-Side / B-Side / Options
    is_aside = models.BooleanField('a-side?', default=False)
    is_bside = models.BooleanField('b-side?', default=False)
    is_album_track = models.BooleanField('album track?', default=False)
    is_instrumental = models.BooleanField('instrumental?', default=False)

    class Meta:
        ordering = ('edition', 'position')
        unique_together = ('edition', 'track', 'is_instrumental')
        verbose_name = 'track'

    def __unicode__(self):
        if self.is_instrumental:
            return u'%s (Instrumental) on %s' % (self.track, self.edition)
        return u'%s on %s' % (self.track, self.edition)


class Video(models.Model):
    VIDEO_TYPES = Choices(
        # Promotional Videos.
        (1, 'pv_regular', 'Regular'),
        (2, 'pv_danceshot', 'Dance Shot'),
        (3, 'pv_closeup', 'Close-up'),
        (4, 'pv_another', 'Another'),
        (9, 'pv_other', 'Other (PV)'),

        # Promotional Videos (Solo Versions).
        (11, 'pv_solo_version', 'Solo'),
        (12, 'pv_solo_closeup', 'Close-up (Solo)'),

        # Making ofs.
        (21, 'making_general', 'Making of'),
        (22, 'making_jacket', 'Jacket Making'),
        (23, 'making_pv', 'PV Making'),

        # Bonus Material.
        (31, 'bonus_backstage', 'Backstage'),
        (32, 'bonus_performance', 'Performance'),

        (99, 'other', 'Other'),
    )

    album = models.ForeignKey(Album, blank=True, null=True, related_name='videos')
    single = models.ForeignKey(Single, blank=True, null=True, related_name='videos')

    # Metadata
    romanized_name = models.CharField()
    name = models.CharField(blank=True)
    kind = models.PositiveSmallIntegerField(choices=VIDEO_TYPES, default=VIDEO_TYPES.pv_regular)
    released = models.DateField(blank=True, null=True)

    # Contents
    still = models.ImageField(blank=True, null=True, upload_to='merchandise/music/videos/')
    video_url = models.URLField(blank=True)

    class Meta:
        get_latest_by = 'released'

    def __unicode__(self):
        return u'%s' % (self.romanized_name)

    @property
    def parent(self):
        return filter(None, [self.album, self.single])[0]

    @property
    def rendered_kind_display(self):
        if self.kind in [1, 2, 3, 4, 9, 11, 12]:
            return 'Music Video'
        if self.kind in [21, 22, 23]:
            return 'Making of'
        if self.kind in [31, 32]:
            return 'Performance'


class VideoTrackOrder(models.Model):
    edition = models.ForeignKey(Edition, related_name='video_order')
    video = models.ForeignKey(Video, related_name='on_edition')
    position = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('edition', 'position')
        unique_together = ('edition', 'video')
        verbose_name = 'video track'

    def __unicode__(self):
        return u'%s on %s' % (self.video, self.edition)
