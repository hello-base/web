from django.urls import re_path
from django.http import Http404

from multiurl import ContinueResolving, multiurl

from .views import VideodiscDetailView


urlpatterns = [
    # MultiURL allows us to unite all of the media under a simpler URL.
    multiurl(
        re_path(r'^discs/(?P<slug>[-\w]+)/$', VideodiscDetailView.as_view(), name='videodisc-detail'),
        catch=(Http404, ContinueResolving)
    ),
]
