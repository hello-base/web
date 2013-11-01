# -*- coding: utf-8 -*-
import pytest

from components.social.youtube.factories import ChannelFactory, VideoFactory
from components.social.youtube.models import Thumbnail, Video
from components.social.youtube.tasks import (fetch_all_videos,
    fetch_latest_videos, fetch_video)

pytestmark = pytest.mark.django_db


def test_fetch_all_videos():
    channel = ChannelFactory(username='revyver')
    fetch_all_videos(channel)
    assert channel.videos.count() > 0
    for video in channel.videos.all():
        assert isinstance(video, Video)


def test_fetch_latest_videos():
    channel = ChannelFactory(username='revyver')
    fetch_latest_videos(channel)
    assert channel.videos.count() > 0
    for video in channel.videos.all():
        assert isinstance(video, Video)


def test_fetch_video():
    video = VideoFactory(ytid='MhH_ucrPMZc')
    fetch_video(video)
    assert 'Morning Musume' in video.title
    assert video.thumbnails.count() > 0
    for thumbnail in video.thumbnails.all():
        assert isinstance(thumbnail, Thumbnail)
