from django.conf.urls import patterns, url
from django.http import Http404
from django.views.generic.base import RedirectView

from multiurl import ContinueResolving, multiurl

from .views import (GroupBrowseView, GroupDetailView, GroupDiscographyView, GroupMembershipView,
    IdolBrowseView, IdolDetailView, IdolDiscographyView, StaffBrowseView, StaffDetailView)


urlpatterns = patterns('',
    # MultiURL allows us to unite all of the music under a simpler URL.
    multiurl(
        url(r'^(?P<slug>[-\w]+)/$', name='group-detail', view=GroupDetailView.as_view()),
        url(r'^(?P<slug>[-\w]+)/$', name='idol-detail', view=IdolDetailView.as_view()),

        # url('^music/(?P<slug>[-\w]+)/$', name='album-detail', view=AlbumDetailView.as_view()),
        # url('^music/(?P<slug>[-\w]+)/$', name='single-detail', view=SingleDetailView.as_view()),
        catch=(Http404, ContinueResolving)
    ),

    url(r'^groups/browse/$', name='group-browse', view=GroupBrowseView.as_view()),
    url(r'^groups/(?P<slug>[-\w]+)/discography/$', name='group-discography', view=GroupDiscographyView.as_view()),
    url(r'^groups/(?P<slug>[-\w]+)/members/$', name='group-membership', view=GroupMembershipView.as_view()),
    url(r'^groups/(?P<slug>[-\w]+)/$', name='group-detail', view=GroupDetailView.as_view()),
    url(r'^groups/$', name='group-list', view=RedirectView.as_view(url='/groups/browse/')),

    url(r'^idols/browse/$', name='idol-browse', view=IdolBrowseView.as_view()),
    url(r'^idols/(?P<slug>[-\w]+)/discography/$', name='idol-discography', view=IdolDiscographyView.as_view()),
    url(r'^idols/(?P<slug>[-\w]+)/$', name='idol-detail', view=IdolDetailView.as_view()),
    url(r'^idols/$', name='idol-list', view=RedirectView.as_view(url='/idols/browse/')),

    url(r'^staff/browse/$', name='staff-browse', view=StaffBrowseView.as_view()),
    url(r'^staff/(?P<slug>[-\w]+)/$', name='staff-detail', view=StaffDetailView.as_view()),
    url(r'^staff/$', name='staff-list', view=RedirectView.as_view(url='/staff/browse/'))
)
