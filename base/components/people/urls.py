from django.conf.urls import patterns, url
from django.http import Http404

from multiurl import ContinueResolving, multiurl

from .views import GroupDetailView, IdolDetailView
from .views import HelloProjectDetailView  # Overrides.


urlpatterns = patterns('',
    url(r'^hello-project/$', name='hello-project', view=HelloProjectDetailView.as_view()),

    # MultiURL allows us to unite all of the people under a simpler URL.
    multiurl(
        url(r'^(?P<slug>[-\w]+)/$', name='idol-detail', view=IdolDetailView.as_view()),
        url(r'^(?P<slug>[-\w]+)/$', name='group-detail', view=GroupDetailView.as_view()),
        catch=(Http404, ContinueResolving)
    ),

    # url(r'^staff/(?P<slug>[-\w]+)/$', name='staff-detail', view=StaffDetailView.as_view()),

    # url(r'^groups/$', name='group-browse', view=GroupBrowseView.as_view()),
    # url(r'^idols/$', name='idol-browse', view=IdolBrowseView.as_view()),
    # url(r'^staff/$', name='staff-browse', view=StaffBrowseView.as_view()),
)
