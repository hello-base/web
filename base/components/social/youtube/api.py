import gdata.youtube.service
import os


class Api:
    service = gdata.youtube.service.YouTubeService()

    def __init__(self):
        self.base_url = 'http://gdata.youtube.com/feeds/api'

    def fetch_video(self, video_id):
        return Api.service.GetYouTubeVideoEntry('%s/users/default/uploads/%s' % (self.base_url, video_id))

    def fetch_feed_by_username(self, username):
        uri = os.sep.join([self.base_url, 'users', username, 'uploads'])
        return Api.service.GetYouTubeVideoFeed(uri)
