import pytest

from components.social.twitter.models import Tweet, TwitterUser
from components.social.twitter.factories import TweetFactory, TwitterUserFactory


pytestmark = pytest.mark.django_db

class TestTwitterUsers:
    def test_twitteruser_factory(self):
        factory = TwitterUserFactory()
        assert isinstance(factory, TwitterUser)


class TestTweets:
    def test_tweet_factory(self):
        user = TwitterUserFactory()
        factory = TweetFactory(user=user)
        assert isinstance(factory, Tweet)
