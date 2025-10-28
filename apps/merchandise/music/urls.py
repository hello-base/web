from django.urls import re_path
from django.http import Http404

from multiurl import ContinueResolving, multiurl

from .views import (AlbumDetailView, SingleDetailView, TrackDetailView,
    TrackLyricsView)


urlpatterns = [
    # MultiURL allows us to unite all of the music under a simpler URL.
    multiurl(
        re_path(r'^music/(?P<slug>[-\w]+)/$', SingleDetailView.as_view(), name='single-detail'),
        re_path(r'^music/(?P<slug>[-\w]+)/$', AlbumDetailView.as_view(), name='album-detail'),
        catch=(Http404, ContinueResolving)
    ),

    # re_path(r'^music/albums/$', AlbumBrowseView.as_view(), name='album-browse'),
    # re_path(r'^music/singles/$', SingleBrowseView.as_view(), name='single-browse'),

    re_path(r'^music/tracks/(?P<slug>[-\w]+)/lyrics/$', TrackLyricsView.as_view(), name='track-lyrics-detail'),
    re_path(r'^music/tracks/(?P<slug>[-\w]+)/$', TrackDetailView.as_view(), name='track-detail'),
    # re_path(r'^music/tracks/$', TrackBrowseView.as_view(), name='track-browse'),

    # re_path(r'^music/$', MusicBrowseView.as_view(), name='music-browse'),
]
