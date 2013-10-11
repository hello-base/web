from base64 import urlsafe_b64encode

from django.core.urlresolvers import reverse
from django.db import models

from model_utils import Choices

from components.people.models import ParticipationMixin
from components.merchandise.media.models import Merchandise


class Videodisc(ParticipationMixin, Merchandise):
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
    )

    kind = models.IntegerField(choices=VIDEO_TYPES, default=VIDEO_TYPES.concert)
    slug = models.SlugField(blank=True)

    def get_absolute_url(self):
        return reverse('videodisc-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        slug = urlsafe_b64encode(self.uuid.bytes)
        self.slug = slug.replace('=', '')
        super(Videodisc, self).save(*args, **kwargs)


class VideodiscFormat(models.Model):
    FORMAT_TYPES = Choices((1, 'dvd', 'DVD'), (2, 'bluray', 'Blu-ray Disc'))
    parent = models.ForeignKey(Videodisc, blank=True, null=True, , related_name='formats')

    # Metadata
    kind = models.IntegerField(choices=FORMAT_TYPES, default=FORMAT_TYPES.dvd)
    released = models.DateField(blank=True, db_index=True, default=date.min, null=True)
    catalog_number = models.CharField(blank=True)

    # Content
    art = models.ImageField(blank=True, null=True, upload_to='merchandise/media/videos/')
    clips = models.ManyToManyField('music.Track', blank=True, null=True, related_name='videos', through='Clip')

    class Meta:
        get_latest_by = 'released'
        ordering = ('-released',)

    def __unicode__(self):
        return u'%s' % (self.parent.romanized_name)
