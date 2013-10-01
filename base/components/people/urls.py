from django.conf.urls import patterns, url
from django.http import Http404
from django.views.generic.base import RedirectView

from multiurl import ContinueResolving, multiurl

from .views import (GroupBrowseView, GroupDetailView,
    GroupMembershipView, IdolBrowseView, IdolDetailView,
    StaffBrowseView, StaffDetailView)


urlpatterns = patterns('',
    # MultiURL allows us to unite all of the music under a simpler URL.
    multiurl(
        url(r'^(?P<slug>[-\w]+)/$', name='group-detail', view=GroupDetailView.as_view()),
        url(r'^(?P<slug>[-\w]+)/$', name='idol-detail', view=IdolDetailView.as_view()),
        catch=(Http404, ContinueResolving)
    ),

    url(r'^groups/browse/$', name='group-browse', view=GroupBrowseView.as_view()),
    url(r'^groups/$', name='group-list', view=RedirectView.as_view(url='/groups/browse/')),

    url(r'^idols/browse/$', name='idol-browse', view=IdolBrowseView.as_view()),
    url(r'^idols/$', name='idol-list', view=RedirectView.as_view(url='/idols/browse/')),

    url(r'^staff/browse/$', name='staff-browse', view=StaffBrowseView.as_view()),
    url(r'^staff/(?P<slug>[-\w]+)/$', name='staff-detail', view=StaffDetailView.as_view()),
    url(r'^staff/$', name='staff-list', view=RedirectView.as_view(url='/staff/browse/'))
)
