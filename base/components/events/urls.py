from django.conf.urls import patterns, url

from .views import (EventDetailView, EventListView, EventCreateView, 
    EventUpdateView, EventGoodsDetailView, VenueListView, VenueDetailView, 
    VenueCreateView, VenueUpdateView)


urlpatterns = patterns('',
    url(r'^events/(?P<slug>[-\w]+)/$', name='event-detail', view=EventDetailView.as_view()),
    url(r'^events/$', name='event-list', view=EventListView.as_view()),
    
    url(r'^venues/(?P<slug>[-\w]+)/$', name='venue-detail', view=VenueDetailView.as_view()),
    url(r'^venues/$', name='venue-list', view=VenueListView.as_view()),
    
    url(r'^event/create/$', name='event-create', view=EventCreateView.as_view()),
    url(r'^event/update/(?P<pk>\d+)/$', name='event-update', view=EventUpdateView.as_view()),
    url(r'^venue/create/$', name='venue-create', view=VenueCreateView.as_view()),
    url(r'^venue/update/(?P<pk>\d+)/$', name='venue-update', view=VenueUpdateView.as_view()),
)
