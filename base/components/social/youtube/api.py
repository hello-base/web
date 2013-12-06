# -*- coding: utf-8 -*-
from apiclient import discovery
from httplib2 import Http

from django.conf import settings


class Api:
    http = Http(cache='.cache')
    developer_key = settings.YOUTUBE_DEVELOPER_KEY
    service = discovery.build('youtube', 'v3', developerKey=developer_key, http=http)

    def get_upload_playlist(self, channel_id):
        channel = Api.service.channels().list(part='contentDetails', id=channel_id).execute()
        return channel['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    def get_ytid(self, username):
        channel = Api.service.channels().list(part='id', forUsername=username).execute()
        return channel['items'][0]['id']

    def get_all_videos(self, channel_id):
        playlist_id = self.get_upload_playlist(channel_id)
        playlist_items = self.service.playlistItems()
        request = playlist_items.list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50
        )

        videos = []
        while request is not None:
            items = request.execute()
            for item in items.get('items', []):
                videos.append(item['contentDetails']['videoId'])
            request = playlist_items.list_next(request, items)
        return videos

    def get_latest_videos(self, channel_id):
        playlist_id = self.get_upload_playlist(channel_id)
        playlist_items = self.service.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id
        ).execute()

        videos = []
        for item in playlist_items.get('items', []):
            videos.append(item['contentDetails']['videoId'])
        return videos

    def get_video(self, video_id):
        video = Api.service.videos().list(part='id,snippet,contentDetails', id=video_id).execute()
        return video['items'][0]
