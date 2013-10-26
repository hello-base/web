import re

from datetime import datetime, timedelta
from time import timezone

from django.utils.html import urlize
from django.utils.timezone import get_default_timezone, make_aware

from celery.decorators import task

from .api import Api
from .models import Tweet, TwitterUser

re_usernames = re.compile("@([0-9a-zA-Z+_]+)", re.IGNORECASE)
re_hashtags = re.compile("#([0-9a-zA-Z+_]+)", re.IGNORECASE)
replace_hashtags = "<a href=\"http://twitter.com/search?q=%23\\1\">#\\1</a>"
replace_usernames = "<a href=\"http://twitter.com/\\1\">@\\1</a>"


@task
def fetch_tweets(**kwargs):
    api = Api()
    date_format = '%a %b %d %H:%M:%S +0000 %Y'

    for user in TwitterUser.objects.all():
        timeline = api.fetch_timeline_by_screen_name(screen_name=user.screen_name)
        for json in timeline:
            tweet_id = json['id']
            tweet, created = Tweet.objects.get_or_create(tweet_id=tweet_id)

            # Do we have a retweet?
            if 'retweeted_status' in json:
                tweet.retweeted = True

                # Process the retweeter.
                retweet_user = json['retweeted_status']['user']
                tweet.retweeter_profile_image_url = retweet_user['profile_iamge_url']
                tweet.retweeter_screen_name = retweet_user['screen_name']
                tweet.retweeter_name = retweet_user['name']

                # Process the retweet.
                retweet = json['retweeted_status']
                tweet.retweeted_status_id = retweet['status_id']
                tweet.retweeted_status_id_str = retweet['status_id_str']
                tweet.retweeted_status_text = retweet['text']
                tweet.retweeted_status_source = retweet['source']

                # Process the date of the original retweet.
                d = datetime.strftime(retweet['created_at'], date_format)
                d -= timedelta(seconds=timezone)
                tweet.retweeted_status_created_at = make_aware(d, get_default_timezone())

            tweet.user = user
            tweet.tweet_id = json['id']
            tweet.tweet_id_str = json['id_str']
            tweet.source = json['source']

            # Store reply metadata.
            tweet.in_reply_to_user_id = json['in_reply_to_user_id']
            tweet.in_reply_to_user_id_str = json['in_reply_to_user_id_str']
            tweet.in_reply_to_status_id = json['in_reply_to_status_id']
            tweet.in_reply_to_status_id_str = json['in_reply_to_status_str']

            # Urlize and linkify hashtags and usernames.
            tweet.text = urlize(json['text'])
            tweet.text = re_usernames.sub(replace_usernames, tweet.text)
            tweet.text = re_hashtags.sub(replace_hashtags, tweet.text)

            # Process the date.
            d = datetime.strptime(json['created_at'], date_format)
            d -= timedelta(seconds=timezone)
            tweet.created_at = make_aware(d, get_default_timezone())
            tweet.save()
