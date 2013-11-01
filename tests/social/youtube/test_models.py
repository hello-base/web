# -*- coding: utf-8 -*-
import gdata.youtube
import pytest

from components.social.youtube.models import Channel, Thumbnail, Video
from components.social.youtube.factories import (ChannelFactory,
    ThumbnailFactory, VideoFactory)

pytestmark = pytest.mark.django_db


class TestChannels:
    def test_factory(self):
        factory = ChannelFactory()
        assert isinstance(factory, Channel)

    def test_fetch_all_videos(self, monkeypatch):
        channel = ChannelFactory(username='revyver')
        entries = channel.entries()
        assert len(entries) > 0
        for entry in entries:
            assert isinstance(entry, gdata.youtube.YouTubeVideoEntry)


class TestVideos:
    def test_factory(self):
        factory = VideoFactory()
        assert isinstance(factory, Video)

    def test_get_absolute_url(self):
        url = 'https://www.youtube.com/watch?v=kZYpUZ1IUlk'
        factory = VideoFactory(watch_url=url)
        assert factory.get_absolute_url() == url

    def test_fetch_video(self):
        video = VideoFactory(ytid='MhH_ucrPMZc')
        entry = video.entry()
        assert isinstance(entry, gdata.youtube.YouTubeVideoEntry)
        assert 'Morning Musume' in entry.title.text


class TestThumbnails:
    def test_factory(self):
        factory = ThumbnailFactory()
        assert isinstance(factory, Thumbnail)

    def test_get_absolute_url(self):
        url = 'https://i1.ytimg.com/vi/kZYpUZ1IUlk/0.jpg'
        factory = ThumbnailFactory(url=url)
        assert factory.get_absolute_url() == url
