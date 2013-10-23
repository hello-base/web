from django.db import models
from django.db.models.signals import post_save

from twitter import Twitter

from components.people.models import Group, Idol


class TwitterUser(models.Model):
    twitter_id = models.PositiveIntegerField(blank=True, null=True)
    screen_name = models.CharField(blank=True, max_length=200)
    name = models.CharField(blank=True, max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(blank=True, max_length=200)
    profile_image_url = models.URLField(blank=True)
    url = models.URLField(blank=True)

    # Optional relationships.
    idols = models.OneToOneField(Idol, blank=True, null=True, related_name='%(class)s')
    groups = models.OneToOneField(Group, blank=True, null=True, related_name='%(class)s')

    def __unicode__(self):
        return u'%s' % (self.screen_name)

    def get_absolute_url(self):
        return 'https://twitter.com/%s' % (self.screen_name)


class Tweet(models.Model):
    user = models.ForeignKey(TwitterUser, related_name='tweets')

    tweet_id = models.BigIntegerField(blank=True, null=True)
    tweet_id_str = models.CharField(blank=True, max_length=200)
    created_at = models.DateTimeField(blank=True, null=True)
    text = models.TextField(blank=True)
    source = models.CharField(blank=True, max_length=200)

    # Replies.
    in_reply_to_user_id = models.BigIntegerField(blank=True, null=True)
    in_reply_to_user_id_str = models.CharField(blank=True, max_length=200)
    in_reply_to_status_id = models.BigIntegerField(blank=True, null=True)
    in_reply_to_status_id_str = models.CharField(blank=True, max_length=200)

    # Retweets.
    retweeted = models.BooleanField(default=False)
    retweeter_profile_image_url = models.URLField(blank=True)
    retweeter_screen_name = models.CharField(blank=True, max_length=200)
    retweeter_name = models.CharField(blank=True, max_length=200)
    retweeted_status_id = models.BigIntegerField(blank=True, null=True)
    retweeted_status_id_str = models.CharField(blank=True, max_length=200)
    retweeted_status_created_at = models.DateTimeField(blank=True, null=True)
    retweeted_status_text = models.TextField(blank=True)
    retweeted_status_source = models.CharField(blank=True, max_length=200)

    def __unicode__(self):
        return u'%s: %s' % (self.user.screen_name, self.text)

    def get_absolute_url(self):
        parts = {'screen_name': self.user.screen_name, 'id': self.tweet_id_str}
        if self.retweeted:
            parts['screen_name'] = self.retweeter_screen_name
            parts['id'] = self.retweeted_status_id_str
        return 'https://twitter.com/%s/status/%s' % (parts['screen_name'], parts['id'])
