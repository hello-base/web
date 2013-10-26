# -*- coding: utf-8 -*-
import pytest

from components.social.youtube.models import Channel, Video
from components.social.youtube.factories import ChannelFactory, VideoFactory

pytestmark = pytest.mark.django_db


class TestChannels:
    def test_channel_factory(self):
        factory = ChannelFactory()
        assert isinstance(factory, Channel)


class TestVideo:
    def test_video_factory(self):
        # We're fetching "Wagamama Ki no Mama Ai no Joke."
        # As such, this test depends on YouTube.
        channel = ChannelFactory()
        factory = VideoFactory(channel=channel, ytid='MhH_ucrPMZc')
        assert isinstance(factory, Video)
        assert 'モーニング娘。' in factory.title
