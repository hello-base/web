# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

import gdata.youtube.service
import os
import urllib
import urlparse

from django.conf import settings


class Api:
    service = gdata.youtube.service.YouTubeService()

    def __init__(self):
        self.developer_key = settings.YOUTUBE_DEVELOPER_KEY
        self.client_id = 'hello-base'
        self.base_url = 'http://gdata.youtube.com/feeds/api'

        Api.service.developer_key = self.developer_key
        Api.service.client_id = self.client_id

    def process_params(self, url, params):
        url_parts = list(urlparse.urlparse(url))
        url_parts[4] = urllib.urlencode(params)
        url = urlparse.urlunparse(url_parts)
        return url

    def fetch_video(self, video_id):
        return Api.service.GetYouTubeVideoEntry(video_id=video_id)

    def fetch_latest_videos_by_username(self, username):
        params = {'start-index': 1, 'max-results': 10}
        url = os.sep.join([self.base_url, 'users', username, 'uploads'])
        url = self.process_params(url, params)
        return Api.service.GetYouTubeVideoFeed(url)

    def fetch_all_videos_by_username(self, username):
        videos = []

        params = {'start-index': 1, 'max-results': 10}
        url = os.sep.join([self.base_url, 'users', username, 'uploads'])
        feed = Api.service.GetYouTubeVideoFeed(self.process_params(url, params))
        videos.extend([video for video in feed.entry])
        total_results = feed.total_results.text

        total_pages = float(total_results) / 10
        current_page = 0
        start_index = 1
        while current_page <= total_pages:
            logger.debug('Fetching feed for %s, page %s' % (username, current_page))
            current_page += 1
            params = {'start-index': start_index, 'max-results': 10}
            feed = Api.service.GetYouTubeVideoFeed(self.process_params(url, params))
            videos.extend([video for video in feed.entry])
            start_index += 10
        return videos
