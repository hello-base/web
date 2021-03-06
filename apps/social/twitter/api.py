from django.conf import settings

from twitter import Twitter, OAuth


class Api:
    service = Twitter(auth=OAuth(
        settings.TWITTER_OAUTH_TOKEN,
        settings.TWITTER_OAUTH_SECRET,
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET
    ))

    def fetch_timeline_by_screen_name(self, screen_name, **kwargs):
        return Api.service.statuses.user_timeline(screen_name=screen_name, **kwargs)
