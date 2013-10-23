from twitter import Twitter, OAuth


class Api:
    service = Twitter(auth=OAuth(
        settings.TWITTER_OAUTH_TOKEN,
        settings.TWITTER_OAUTH_SECRET,
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET
    ))

    def fetch_timeline_by_screen_name(self, screen_name):
        return Api.service.statuses.user_timeline(screen_name=screen_name)

    def fetch_user_by_screen_name(self, screen_name):
        return Api.service.users.show(screen_name=screen_name)

    def fetch_user_by_twitter_id(self, twitter_id):
        return Api.service.users.show(twitter_id=twitter_id)
