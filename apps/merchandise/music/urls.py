from django.conf.urls import patterns, url
from django.http import Http404

from multiurl import ContinueResolving, multiurl

from .views import (AlbumDetailView, SingleDetailView, TrackDetailView,
    TrackLyricsView)


urlpatterns = patterns('',
    # MultiURL allows us to unite all of the music under a simpler URL.
    multiurl(
        url(r'^music/(?P<slug>[-\w]+)/$', name='single-detail', view=SingleDetailView.as_view()),
        url(r'^music/(?P<slug>[-\w]+)/$', name='album-detail', view=AlbumDetailView.as_view()),
        catch=(Http404, ContinueResolving)
    ),

    # url(r'^music/albums/$', name='album-browse', view=AlbumBrowseView.as_view()),
    # url(r'^music/singles/$', name='single-browse', view=SingleBrowseView.as_view()),

    url(r'^music/tracks/(?P<slug>[-\w]+)/lyrics/$', name='track-lyrics-detail', view=TrackLyricsView.as_view()),
    url(r'^music/tracks/(?P<slug>[-\w]+)/$', name='track-detail', view=TrackDetailView.as_view()),
    # url(r'^music/tracks/$', name='track-browse', view=TrackBrowseView.as_view()),

    # url(r'^music/$', name='music-browse', view=MusicBrowseView.as_view()),
)
