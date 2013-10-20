from dateutil import parser

from django.db import models

from .api import Api


class Channel(models.Model):
    username = models.CharField()

    # Optional relationships.
    idols = models.ManyToManyField(Idol, blank=True, null=True, related_name='%(class)ss')
    groups = models.ManyToManyField(Group, blank=True, null=True, related_name='%(class)ss')

    def __unicode__(self):
        return u'%s' % (self.username)


class Video(models.Model):
    channel = models.ForeignKey(Channel, related_name='videos')

    # Metadata.
    title = models.CharField(blank=True, max_length=200)
    description = models.TextField(blank=True)
    published = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)

    ytid = models.CharField(blank=True, max_length=200, unique=True)
    flash_url = models.URLField(blank=True)
    watch_url = models.URLField(blank=True)

    def __unicode__(self):
        return u'%s' % (self.title)

    def get_absolute_url(self):
        return self.watch_url

    def save(self, *args, **kwargs):
        if not self.id:
            # Connect to API and get the details.
            entry = self.entry()

            # Set the details.
            self.title = entry.media.title.text
            self.description = entry.media.description.text
            self.published = parser.parse(entry.published.text)
            self.duration = entry.media.duration.seconds
            self.flash_url = entry.GetSwfUrl()
            self.watch_url = entry.media.player.url

            # Save the instance.
            return super(Video, self).save(*args, **kwargs)

            # Save the thumbnails.
            for thumbnail in entry.media.thumbnail:
                t = Thumbnail()
                t.url = thumbnail.url
                t.video = self
                t.save()

    def entry(self):
        api = Api()
        return api.fetch_video(self.ytid)


class Thumbnail(models.Model):
    video = models.ForeignKey(Video, null=True, related_name='thumbnails')
    url = models.URLField()

    def __unicode__(self):
        return u'%s (for %s)' % (self.url, self.video.title)

    def get_absolute_url(self):
        return self.url
