from django.urls import re_path

from .views import (EventDetailView, EventListView, VenueListView,
    VenueDetailView)


urlpatterns = [
    re_path(r'^events/(?P<slug>[-\w]+)/$', EventDetailView.as_view(), name='event-detail'),
    re_path(r'^events/$', EventListView.as_view(), name='event-list'),

    re_path(r'^venues/(?P<slug>[-\w]+)/$', VenueDetailView.as_view(), name='venue-detail'),
    re_path(r'^venues/$', VenueListView.as_view(), name='venue-list'),
]
