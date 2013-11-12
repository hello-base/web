# -*- coding: utf-8 -*-
import pytest

from components.social.twitter.factories import TwitterUserFactory
from components.social.twitter.tasks import fetch_tweets

pytestmark = pytest.mark.django_db


def test_fetch_tweets():
    tweeter = TwitterUserFactory(screen_name='hello_base')
    fetch_tweets()
    assert tweeter.tweets.count > 0
