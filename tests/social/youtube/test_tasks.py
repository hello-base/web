# -*- coding: utf-8 -*-
import pytest

from apps.social.youtube.factories import ChannelFactory
from apps.social.youtube.models import Video
from apps.social.youtube.tasks import (fetch_all_videos,
    fetch_latest_videos)

pytestmark = pytest.mark.django_db


def test_fetch_all_videos():
    channel = ChannelFactory()
    fetch_all_videos(channel)
    assert channel.videos.count() > 0
    for video in channel.videos.all():
        assert isinstance(video, Video)


def test_fetch_latest_videos():
    channel = ChannelFactory()
    fetch_latest_videos()
    assert channel.videos.count() > 0
    for video in channel.videos.all():
        assert isinstance(video, Video)
