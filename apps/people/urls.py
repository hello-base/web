from django.urls import re_path
from django.http import Http404

from multiurl import ContinueResolving, multiurl

from .views import GroupDetailView, IdolDetailView


urlpatterns = [
    # MultiURL allows us to unite all of the people under a simpler URL.
    multiurl(
        re_path(r'^(?P<slug>[-\w]+)/$', IdolDetailView.as_view(), name='idol-detail'),
        re_path(r'^(?P<slug>[-\w]+)/$', GroupDetailView.as_view(), name='group-detail'),
        catch=(Http404, ContinueResolving)
    ),

    # re_path(r'^staff/(?P<slug>[-\w]+)/$', StaffDetailView.as_view(), name='staff-detail'),

    # re_path(r'^groups/$', GroupBrowseView.as_view(), name='group-browse'),
    # re_path(r'^idols/$', IdolBrowseView.as_view(), name='idol-browse'),
    # re_path(r'^staff/$', StaffBrowseView.as_view(), name='staff-browse'),
]
