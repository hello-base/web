# -*- coding: utf-8 -*-
import pytest

from base.apps.social.youtube.models import Channel, Thumbnail, Video
from base.apps.social.youtube.factories import (ChannelFactory,
    ThumbnailFactory, VideoFactory)

pytestmark = pytest.mark.django_db


class TestChannels:
    def test_factory(self):
        factory = ChannelFactory(ytid='')
        assert isinstance(factory, Channel)
        assert factory.ytid == 'UCZEFNpu29g_QBqkNC619tEA'


class TestVideos:
    @pytest.fixture
    def video(self):
        return VideoFactory(ytid='lmXS7cypzCI')

    def test_factory(self, video):
        assert isinstance(video, Video)
        assert 'Hello! Party' in video.title
        assert video.thumbnails.count() > 0
        for thumbnail in video.thumbnails.all():
            assert isinstance(thumbnail, Thumbnail)

    def test_get_absolute_url(self, video):
        url = 'http://youtu.be/lmXS7cypzCI'
        assert video.get_absolute_url() == url

    def test_entry(self, video):
        entry = video.entry()
        assert 'Hello! Party' in entry['snippet']['title']
        assert 'PT1M27S' in entry['contentDetails']['duration']


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
