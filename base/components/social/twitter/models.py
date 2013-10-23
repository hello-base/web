from twitter import Twitter

from django.db import models
from django.db.models.signals import post_save


class TwitterUser(models.Model):
    twitter_id = models.PositiveIntegerField(blank=True, null=True)
    screen_name = models.CharField(blank=True, max_length=200)
    name = models.CharField(blank=True, max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(blank=True, max_length=200)
    avatar = models.URLField(blank=True)
    url = models.URLField(blank=True)

    # Optional relationships.
    idols = models.OneToOneField(Idol, blank=True, null=True, related_name='%(class)s')
    groups = models.OneToOneField(Group, blank=True, null=True, related_name='%(class)s')

    def __unicode__(self):
        return u'%s' % (self.screen_name)

    def get_absolute_url(self):
        return 'https://twitter.com/%s' % (self.screen_name)


class Tweet(models.Model):
    pass
