import pytest

from components.social.twitter.models import Tweet, TwitterUser
from components.social.twitter.factories import TweetFactory, TwitterUserFactory


pytestmark = pytest.mark.django_db

class TestTwitterUsers:
    def test_twitteruser_factory():
        factory = TwitterUserFactory()
        assert isinstance(factory, TwitterUser)


class TestTweets:
    def test_twitteruser_factory():
        factory = TweetFactory()
        assert isinstance(factory, Tweet)
