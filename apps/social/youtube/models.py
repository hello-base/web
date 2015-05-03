# -*- coding: utf-8 -*-
from dateutil import parser

from django.db import models

from apps.people.models import Group, Idol


class Channel(models.Model):
    username = models.CharField(max_length=60)
    ytid = models.CharField('YouTube ID', blank=True, max_length=60)

    # Optional relationships.
    idol = models.OneToOneField(Idol, blank=True, null=True, related_name='%(class)s')
    group = models.OneToOneField(Group, blank=True, null=True, related_name='%(class)s')

    def __unicode__(self):
        return u'%s' % (self.username)

    def save(self, *args, **kwargs):
        from .api import Api

        if not self.ytid:
            api = Api()
            self.ytid = api.get_ytid(self.username)
        super(Channel, self).save(*args, **kwargs)
        from .tasks import fetch_all_videos
        fetch_all_videos.delay(self.username)


class Video(models.Model):
    ytid = models.CharField('YouTube ID', max_length=200, primary_key=True, unique=True)
    channel = models.ForeignKey(Channel, related_name='videos')

    # Metadata.
    title = models.CharField(blank=True, max_length=200)
    description = models.TextField(blank=True, null=True)
    published = models.DateTimeField(blank=True, null=True)
    duration = models.CharField(blank=True, max_length=10, null=True)

    def __unicode__(self):
        return u'%s' % (self.title)

    def get_absolute_url(self):
        return 'http://youtu.be/%s' % (self.ytid)

    def save(self, *args, **kwargs):

        # Connect to API and get the details.
        entry = self.entry()

        # Set the details.
        self.title = entry['snippet']['title']
        self.description = entry['snippet']['description']
        self.published = parser.parse(entry['snippet']['publishedAt'])
        self.duration = entry['contentDetails']['duration']
        super(Video, self).save(*args, **kwargs)

        # Save the thumbnails.
        thumbnails = entry['snippet']['thumbnails']
        for key, value in thumbnails.iteritems():
            t, created = Thumbnail.objects.get_or_create(video=self, quality=key, url=value['url'])
            t.save()

    def entry(self):
        from .api import Api

        api = Api()
        return api.get_video(self.ytid)


class Thumbnail(models.Model):
    video = models.ForeignKey(Video, null=True, related_name='thumbnails')
    quality = models.CharField(default='default', max_length=10)
    url = models.URLField('URL')

    def __unicode__(self):
        return u'%s (for %s)' % (self.url, self.video.title)

    def get_absolute_url(self):
        return self.url
