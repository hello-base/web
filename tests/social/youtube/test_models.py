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

    def test_fetch_all_videos(self):
        channel = ChannelFactory(username='revyver')
        entries = channel.entries()
        assert len(entries) > 0
        for entry in entries:
            assert isinstance(entry, gdata.youtube.YouTubeVideoEntry)

    def test_fetch_latest_videos(self):
        channel = ChannelFactory(username='revyver')
        entries = channel.latest_entries()
        assert isinstance(entries, gdata.youtube.YouTubeVideoFeed)
        assert len(entries.entry) == 10


class TestVideos:
    def test_factory(self):
        factory = VideoFactory(ytid='MhH_ucrPMZc')
        assert isinstance(factory, Video)
        assert 'Morning Musume' in factory.title
        assert factory.thumbnails.count() > 0
        for thumbnail in factory.thumbnails.all():
            assert isinstance(thumbnail, Thumbnail)

    def test_get_absolute_url(self):
        url = 'https://www.youtube.com/watch?v=MhH_ucrPMZc&feature=youtube_gdata_player'
        factory = VideoFactory(ytid='MhH_ucrPMZc', watch_url=url)
        assert factory.get_absolute_url() == url

    def test_fetch_video(self):
        video = VideoFactory(ytid='MhH_ucrPMZc')
        entry = video.entry()
        assert isinstance(entry, gdata.youtube.YouTubeVideoEntry)
        assert 'Morning Musume' in entry.title.text


class TestThumbnails:
    def test_factory(self):
        video = VideoFactory(ytid='kZYpUZ1IUlk')
        factory = ThumbnailFactory(video=video)
        assert isinstance(factory, Thumbnail)

    def test_get_absolute_url(self):
        url = 'https://i1.ytimg.com/vi/kZYpUZ1IUlk/0.jpg'
        video = VideoFactory(ytid='kZYpUZ1IUlk')
        factory = ThumbnailFactory(video=video, url=url)
        assert factory.get_absolute_url() == url
