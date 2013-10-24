import gdata.youtube.service
import os

from django.conf import settings


class Api:
    service = gdata.youtube.service.YouTubeService()

    def __init__(self):
        self.developer_key = settings.YOUTUBE_DEVELOPER_KEY
        self.client_id = 'hello-base'
        self.base_url = 'http://gdata.youtube.com/feeds/api'

        Api.service.developer_key = self.developer_key
        Api.service.client_id = self.client_id

    def fetch_video(self, video_id):
        return Api.service.GetYouTubeVideoEntry(video_id=video_id)

    def fetch_feed_by_username(self, username):
        uri = os.sep.join([self.base_url, 'users', username, 'uploads'])
        return Api.service.GetYouTubeVideoFeed(uri)
