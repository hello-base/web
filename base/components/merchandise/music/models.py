from datetime import date
from itertools import chain

# from ohashi.db import models
# from ...people.constants import CLASSIFICATIONS
# from .managers import (AlbumManager, EditionManager, SingleManager,
#     TrackOrderManager, VideoTrackOrderManager)

from django.core.cache import cache
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel
from ohashi.constants import OTHER
from ohashi.db import models

from ..models import Merchandise


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

    def _render_participants(self):
        groups = self.groups.exclude(classification=CLASSIFICATIONS.supergroup)
        if bool(groups):
            # Gather all of the individual idols attributed to the single
            # into a set().
            idols = set(idol for idol in self.idols.all())

            # Specify an empty set() that will contain all of the members of
            # the groups attributed to the single. Then, loop through all of
            # the groups and update the set with all of the
            # individual members.
            group_members = set()
            for group in groups:
                group_members.update(idol for idol in group.members.all())

            # Simple set() subtraction. We'll be printing whomever's left.
            distinct_idols = idols - group_members
            return list(chain(distinct_idols, groups))
        return self.idols.all()

    @property
    def identifier(self):
        return self._meta.module_name

    def participants(self):
        participants = self._render_participants()
        return participants

    def supergroup(self):
        for group in self.groups.all():
            if group.classification == CLASSIFICATIONS.supergroup:
                return group


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


class Edition(TimeStampedModel):
    REGULAR_ETC, REGULAR, LIMITED_ETC, LIMITED_A, LIMITED_B, LIMITED_C, \
    LIMITED_D, SINGLE_V, EVENT_V, COMMEMORATIVE, DIGITAL = range(1, 12)
    EDITIONS = (
        ('Regular', (
            (REGULAR, 'Regular'),
            (REGULAR_ETC, 'Regular (Other Format)'),
        )),
        ('Limited', (
            (LIMITED_A, 'Limited A'),
            (LIMITED_B, 'Limited B'),
            (LIMITED_C, 'Limited C'),
            (LIMITED_D, 'Limited D'),
            (LIMITED_ETC, 'Limited (Other Format)'),
        )),
        ('Special', (
            (COMMEMORATIVE, 'Commemorative'),
            (DIGITAL, 'Digital'),
            (EVENT_V, 'Event V'),
            (SINGLE_V, 'Single V')
        )),
        (OTHER, 'Other')
    )

    album = models.ForeignKey(Album, blank=True, null=True, related_name='editions')
    single = models.ForeignKey(Single, blank=True, null=True, related_name='editions')

    # Metadata
    romanized_name = models.CharField(blank=True)
    name = models.CharField(blank=True)
    kind = models.IntegerField(choices=EDITIONS, db_index=True, default=REGULAR)
    released = models.DateField(blank=True, db_index=True, null=True)
    catalog_number = models.CharField(blank=True)
    price = models.IntegerField(blank=True, null=True)

    # Contents
    art = models.ImageField(blank=True, null=True, upload_to='releases/music/editions/')
    tracks = models.ManyToManyField('Track', blank=True, null=True, related_name='editions', through='TrackOrder')
    videos = models.ManyToManyField('Video', blank=True, null=True, related_name='editions', through='VideoTrackOrder')

    class Meta:
        get_latest_by = 'released'
        ordering = ('kind',)

    def __unicode__(self):
        if self.parent:
            return u'%s [%s]' % (self.parent.romanized_name, self.romanized_name)
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        if not self.romanized_name:
            self.romanized_name = self.get_kind_display()
        if self.kind in [self.REGULAR, self.DIGITAL]:
            if self.released:
                self.parent.released = self.released
                self.parent.save()
            elif not self.released:
                self.released = date.min
        elif not self.released:
            self.released = self._render_release_date()
        return super(Edition, self).save(*args, **kwargs)

    def _get_regular_edition(self):
        kwargs = {self.parent.identifier: self.parent, 'kind': self.REGULAR}
        return self._default_manager.get(**kwargs)

    def _render_release_date(self):
        return self._get_regular_edition().released

    def _render_tracklist(self):
        if self.kind is not self.REGULAR and not self.order.exists():
            return self._get_regular_edition().order.all()
        return self.order.all()

    def participants(self):
        return self.parent.participants()

    @property
    def parent(self):
        return filter(None, [self.album, self.single])[0]

    def tracklist(self):
        if self.kind in [self.EVENT_V, self.SINGLE_V]:
            return self.order.none()

        tracklist = self._render_tracklist()
        return tracklist


class Track(TimeStampedModel):
    idols = models.ManyToManyField('people.Idol', blank=True, null=True, related_name='tracks')
    groups = models.ManyToManyField('people.Group', blank=True, null=True, related_name='tracks')

    # Metadata
    romanized_name = models.CharField()
    name = models.CharField(blank=True)

    # Alternate Versions
    is_cover = models.BooleanField('cover?', default=False)
    is_alternate = models.BooleanField('alternate?', default=False)
    romanized_name_alternate = models.CharField('alternate name (romanized)', blank=True)
    name_alternate = models.CharField('alternate name', blank=True)

    # Staff
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


class Video(TimeStampedModel):
    PV_NORMAL, PV_ALTERNATE, PV_ANOTHER, PV_CLOSE, PV_CLOSE_SOLO, PV_DANCE, \
    PV_OFFSHOT, PV_SOLO, MO_GENERAL, MO_JACKET, MO_PROMOTIONAL, BACKSTAGE, \
    PERFORMANCE = range(1, 14)
    VIDEO_TYPES = (
        ('Promotional Videos', (
            (PV_NORMAL, 'Normal'),
            (PV_ALTERNATE, 'Alternate (Other)'),
            (PV_ANOTHER, '"Another" Version (Re-Cut)'),
            (PV_CLOSE, 'Close-up'),
            (PV_CLOSE_SOLO, 'Close-up (Solo)'),
            (PV_DANCE, 'Dance Shot'),
            (PV_OFFSHOT, 'Off Shot'),
            (PV_SOLO, 'Solo'),
        )),
        ('Making Of', (
            (MO_GENERAL, 'General'),
            (MO_JACKET, 'Release Jacket'),
            (MO_PROMOTIONAL, 'Promotional Video'),
        )),
        (BACKSTAGE, 'Backstage'),
        (PERFORMANCE, 'Performance'),
        (OTHER, 'Other')
    )

    album = models.ForeignKey(Album, blank=True, null=True, related_name='videos')
    single = models.ForeignKey(Single, blank=True, null=True, related_name='videos')

    # Metadata
    romanized_name = models.CharField()
    name = models.CharField(blank=True)
    kind = models.PositiveSmallIntegerField(choices=VIDEO_TYPES, default=PV_NORMAL)
    released = models.DateField(blank=True, null=True)

    # Contents
    still = models.ImageField(blank=True, null=True, upload_to='releases/music/videos/')
    video_url = models.URLField(blank=True)

    class Meta:
        get_latest_by = 'released'
        ordering = ('-modified',)

    def __unicode__(self):
        return u'%s' % (self.romanized_name)

    @property
    def parent(self):
        return filter(None, [self.album, self.single])[0]


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
