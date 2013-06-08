from django.conf.urls import patterns, url

from .views import EventDetailView, EventListView


urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', name='event-detail', view=EventDetailView.as_view()),
    url(r'^$', name='event-list', view=EventListView.as_view()),
)
