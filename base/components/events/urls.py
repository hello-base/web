from django.conf.urls import patterns, url

from .views import (EventDetailView, EventListView, VenueListView,
    VenueDetailView)


urlpatterns = patterns('',
    url(r'^events/(?P<slug>[-\w]+)/$', name='event-detail', view=EventDetailView.as_view()),
    url(r'^events/$', name='event-list', view=EventListView.as_view()),

    url(r'^venues/(?P<slug>[-\w]+)/$', name='venue-detail', view=VenueDetailView.as_view()),
    url(r'^venues/$', name='venue-list', view=VenueListView.as_view()),
)
