from django.conf.urls import patterns, urls
from django.http import Http404

from multiurl import ContinueResolving, multiurl

from .views import VideodiscDetailView


urlpatterns = patterns('',
    # MultiURL allows us to unite all of the media under a simpler URL.
    multiurl(
        url('^media/(?P<slug>[-\w]+)/$', name='videodisc-detail', view=VideodiscDetailView.as_view()),
    ),
)
