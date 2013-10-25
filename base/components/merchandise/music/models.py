from datetime import date
from itertools import chain
from operator import attrgetter

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from model_utils import Choices
from model_utils.managers import PassThroughManager
from ohashi.constants import OTHER
from ohashi.db import models

from components.merchandise.models import Merchandise
from components.merchandise.utils import uuid_encode
from components.people.models import ParticipationMixin

from .managers import EditionManager, TrackQuerySet, TrackOrderQuerySet


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

    # Denormalized Fields.
    # Note: These fields should be 1) too frequently accessed to make
    # sense as methods and 2) infrequently updated.
    art = models.ImageField(blank=True, null=True, upload_to='merchandise/music/editions/')
    art_thumbnail = ImageSpecField(source='art', processors=[ResizeToFit(width=300)], format='JPEG', options={'quality': 70})

    class Meta:
        abstract = True
        get_latest_by = 'released'
        ordering = ('-released',)

    def __unicode__(self):
        return u'%s' % (self.romanized_name)

    def save(self, *args, **kwargs):
        if self.editions.exists() and self.regular_edition:
            self.art = self.regular_edition.art
            self.released = self.regular_edition.released
        super(Base, self).save(*args, **kwargs)

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains', 'romanized_name__icontains')

    @property
    def identifier(self):
        return self._meta.module_name

    @cached_property
    def participants(self):
        return list(chain(self.participating_idols.all(), self.participating_groups.all()))

    @cached_property
    def regular_edition(self):
        return self.editions.regular_edition(release=self)


class Album(Base):
    is_compilation = models.BooleanField('compilation?', default=False)

    def get_absolute_url(self):
        return reverse('album-detail', kwargs={'slug': self.slug})

    @cached_property
    def get_previous(self):
        if self.number:
            try:
                group = self.groups.get()
                qs = group.albums.order_by('-released').exclude(number='')
                return qs.filter(released__lt=self.released)[0]
            except IndexError:
                return None

    @cached_property
    def get_next(self):
        if self.number:
            try:
                group = self.groups.get()
                qs = group.albums.order_by('released').exclude(number='')
                return qs.filter(released__gt=self.released)[0]
            except IndexError:
                return None


class Single(Base):
    is_indie = models.BooleanField('indie single?', default=False)
    has_8cm = models.BooleanField('8cm version?', default=False)
    has_lp = models.BooleanField('LP version?', default=False)
    has_cassette = models.BooleanField('cassette version?', default=False)

    def get_absolute_url(self):
        return reverse('single-detail', kwargs={'slug': self.slug})

    @cached_property
    def get_previous(self):
        if self.number:
            try:
                group = self.groups.get()
                qs = group.singles.order_by('-released').exclude(number='')
                return qs.filter(released__lt=self.released)[0]
            except IndexError:
                return None

    @cached_property
    def get_next(self):
        if self.number:
            try:
                group = self.groups.get()
                qs = group.singles.order_by('released').exclude(number='')
                return qs.filter(released__gt=self.released)[0]
            except IndexError:
                return None


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
    # Model Managers.
    objects = EditionManager()

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
    art_thumbnail = ImageSpecField(source='art', processors=[ResizeToFit(width=300)], format='JPEG', options={'quality': 70})
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
        if self.kind in [self.EDITIONS.regular, self.EDITIONS.digital] and self.art:
            self.parent.art = self.art
            self.parent.save()
        return super(Edition, self).save(*args, **kwargs)

    def _get_regular_edition(self):
        return self._default_manager.regular_edition(edition=self)

    def _render_release_date(self):
        return self._get_regular_edition().released

    def _render_tracklist(self):
        if self.kind != self.EDITIONS.regular and not self.order.exists():
            return self._get_regular_edition().order.select_related('track')
        return self.order.select_related('track').prefetch_related('track__participating_idols')

    def _render_videolist(self):
        return self.video_order.select_related('video')

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

    @cached_property
    def videolist(self):
        videolist = self._render_videolist()
        return videolist


class Track(ParticipationMixin):
    # Model Managers.
    objects = PassThroughManager.for_queryset_class(TrackQuerySet)()

    album = models.ForeignKey(Album, blank=True, null=True, related_name='tracks')
    single = models.ForeignKey(Single, blank=True, null=True, related_name='tracks')

    # Metadata.
    romanized_name = models.CharField()
    name = models.CharField(blank=True)
    translated_name = models.CharField(blank=True)

    # Alternate Versions.
    original_track = models.ForeignKey('self', blank=True, null=True, related_name='children',
        help_text='If this track is a cover or alternate, choose the original track it\'s based off of.')
    is_cover = models.BooleanField('cover?', default=False)
    is_alternate = models.BooleanField('alternate?', default=False)
    romanized_name_alternate = models.CharField('alternate name (romanized)', blank=True)
    name_alternate = models.CharField('alternate name', blank=True)

    # Lyrics.
    lyrics = models.TextField(blank=True)
    romanized_lyrics = models.TextField(blank=True)
    translated_lyrics = models.TextField(blank=True)
    translation_notes = models.TextField(blank=True)

    # Staff.
    composers = models.ManyToManyField('people.Staff', blank=True, null=True, related_name='composed')
    lyricists = models.ManyToManyField('people.Staff', blank=True, null=True, related_name='wrote')
    arrangers = models.ManyToManyField('people.Staff', blank=True, null=True, related_name='arranged')

    # Secondary identifier.
    uuid = models.UUIDField(auto_add=True, blank=True, null=True)
    slug = models.SlugField(blank=True)

    def __unicode__(self):
        if self.is_alternate:
            if self.is_cover:
                return u'%s [%s, Cover]' % (self.romanized_name, self.romanized_name_alternate)
            return u'%s [%s]' % (self.romanized_name, self.romanized_name_alternate)
        if self.is_cover and not self.is_alternate:
            return u'%s [Cover]' % (self.romanized_name)
        return u'%s [Original]' % (self.romanized_name)

    def get_absolute_url(self):
        if self.original_track:
            return reverse('track-detail', kwargs={'slug': self.original_track.slug})
        return reverse('track-detail', kwargs={'slug': self.slug})

    @cached_property
    def appearances(self):
        appearances = {}
        children = list(self.children.all())
        children.sort(key=attrgetter('parent.released'))

        # Append all of the releases that this track appears on,
        # including looping through all of the tracks that this
        # track is an original of (if applicable).
        appearances['count'] = len(children) + 1
        appearances['debut'] = self.parent
        appearances['children'] = [(track.parent, track) for track in children]
        return appearances

    @property
    def parent(self):
        return filter(None, [self.album, self.single])[0]

    @cached_property
    def participants(self):
        return list(chain(self.participating_idols.all(), self.participating_groups.all()))

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains', 'romanized_name__icontains')


class TrackOrder(models.Model):
    # Model Managers.
    objects = PassThroughManager.for_queryset_class(TrackOrderQuerySet)()

    edition = models.ForeignKey(Edition, related_name='order')
    track = models.ForeignKey(Track, related_name='appears_on')
    position = models.PositiveSmallIntegerField()

    # A-Side / B-Side / Options
    is_aside = models.BooleanField('a-side?', default=False)
    is_bside = models.BooleanField('b-side?', default=False)
    is_album_only = models.BooleanField('album only?', default=False)
    is_instrumental = models.BooleanField('instrumental?', default=False)

    class Meta:
        ordering = ('position',)
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
    video_url = models.URLField('video URL', blank=True)

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
        elif self.kind in [21, 22, 23]:
            return 'Making of'
        elif self.kind in [31, 32]:
            return 'Performance'
        else:
            return ''

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains', 'romanized_name__icontains')


class VideoTrackOrder(models.Model):
    edition = models.ForeignKey(Edition, related_name='video_order')
    video = models.ForeignKey(Video, related_name='on_edition')
    position = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('position',)
        unique_together = ('edition', 'video')
        verbose_name = 'video track'

    def __unicode__(self):
        return u'%s on %s' % (self.video, self.edition)


@receiver(post_save, sender=Track)
def create_slug(sender, instance, created, **kwargs):
    from django.template.defaultfilters import slugify

    if created:
        # Calculate the slug, but only if the track is
        # an original track.
        instance.slug = '' if instance.original_track else slugify(instance.romanized_name)
        instance.save()
    return
