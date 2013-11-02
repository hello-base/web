# -*- coding: utf-8 -*-
from dateutil import parser

from django.db import models
from django.utils.encoding import smart_unicode

from components.people.models import Group, Idol

from .api import Api


class Channel(models.Model):
    username = models.CharField(max_length=60)

    # Optional relationships.
    idol = models.OneToOneField(Idol, blank=True, null=True, related_name='%(class)s')
    group = models.OneToOneField(Group, blank=True, null=True, related_name='%(class)s')

    def __unicode__(self):
        return u'%s' % (self.username)

    def save(self, *args, **kwargs):
        super(Channel, self).save(*args, **kwargs)
        from .tasks import fetch_all_videos
        fetch_all_videos.delay(self)

    def entries(self):
        api = Api()
        return api.fetch_all_videos_by_username(self.username)

    def latest_entries(self):
        api = Api()
        return api.fetch_latest_videos_by_username(self.username)


class Video(models.Model):
    ytid = models.CharField('YouTube ID', max_length=200, primary_key=True, unique=True)
    channel = models.ForeignKey(Channel, related_name='videos')

    # Metadata.
    title = models.CharField(blank=True, max_length=200)
    description = models.TextField(blank=True)
    published = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)

    flash_url = models.URLField('flash URL', blank=True)
    watch_url = models.URLField('watch URL', blank=True)

    def __unicode__(self):
        return u'%s' % (self.title)

    def get_absolute_url(self):
        return self.watch_url

    def save(self, *args, **kwargs):
        # Connect to API and get the details.
        entry = self.entry()

        # Set the details.
        self.title = smart_unicode(entry.media.title.text)
        self.description = entry.media.description.text
        self.published = parser.parse(entry.published.text)
        self.duration = entry.media.duration.seconds
        self.flash_url = entry.GetSwfUrl()
        self.watch_url = entry.media.player.url
        super(Video, self).save(*args, **kwargs)

        # Save the thumbnails.
        for thumbnail in entry.media.thumbnail:
            t = Thumbnail.objects.get_or_create(video=self, url=thumbnail.url)
            t.save()

    def entry(self):
        api = Api()
        return api.fetch_video(self.ytid)


class Thumbnail(models.Model):
    video = models.ForeignKey(Video, null=True, related_name='thumbnails')
    url = models.URLField('URL')

    def __unicode__(self):
        return u'%s (for %s)' % (self.url, self.video.title)

    def get_absolute_url(self):
        return self.url
