import pytest

from components.social.twitter.models import Tweet, TwitterUser
from components.social.twitter.factories import TweetFactory, TwitterUserFactory

pytestmark = pytest.mark.django_db


class TestTwitterUsers:
    def test_factory(self):
        factory = TwitterUserFactory()
        assert isinstance(factory, TwitterUser)

    def test_get_absolute_url(self):
        factory = TwitterUserFactory(screen_name='hello_base')
        assert factory.get_absolute_url() == 'https://twitter.com/hello_base'


class TestTweets:
    def test_factory(self):
        factory = TweetFactory()
        assert isinstance(factory, Tweet)

    def test_get_absolute_url(self):
        user = TwitterUserFactory(screen_name='hello_base')
        tweet = TweetFactory(user=user, tweet_id_str='1')
        assert tweet.get_absolute_url() == 'https://twitter.com/hello_base/status/1'

        retweet = TweetFactory(retweeted=True, retweeter_screen_name='bryanveloso', retweeted_status_id_str='2')
        assert retweet.get_absolute_url() == 'https://twitter.com/bryanveloso/status/2'
