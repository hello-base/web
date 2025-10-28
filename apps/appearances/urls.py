from django.urls import re_path

from .views import (ShowListView, ShowDetailView, EpisodeDetailView,
    MagazineListView, MagazineDetailView, IssueDetailView)


urlpatterns = [

    re_path(r'^show/(?P<slug>[-\w]+)/$', ShowDetailView.as_view(), name='show-detail'),
    re_path(r'^show/$', ShowListView.as_view(), name='show-list'),

    re_path(r'^show/(?P<slug>[-\w]+)/(?P<year>d{4})-(?P<month>d{2})-(?P<day>d+)/$', EpisodeDetailView.as_view(), name='episode-detail'),

    re_path(r'^magazine/(?P<slug>[-\w]+)/$', MagazineDetailView.as_view(), name='magazine-detail'),
    re_path(r'^magazine/$', MagazineListView.as_view(), name='magazine-list'),

    re_path(r'^magazine/issue/(?P<volume_number>[\d\+]+)/$', IssueDetailView.as_view(), name='issue-detail'),
]
