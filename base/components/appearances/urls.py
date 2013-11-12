from django.conf.urls import patterns, url

from .views import (ShowListView, ShowDetailView, EpisodeDetailView,
    MagazineListView, MagazineDetailView, IssueDetailView)


urlpatterns = patterns('',

    url(r'^show/(?P<slug>[-\w]+)/$', name='show-detail', view=ShowDetailView.as_view()),
    url(r'^show/$', name='show-list', view=ShowListView.as_view()),

    url(r'^show/(?P<slug>[-\w]+)/(?P<year>d{4})-(?P<month>d{2})-(?P<day>d+)/$', name='episode-detail', view=EpisodeDetailView.as_view()),

    url(r'^magazine/(?P<slug>[-\w]+)/$', name='magazine-detail', view=MagazineDetailView.as_view()),
    url(r'^magazine/$', name='magazine-list', view=MagazineListView.as_view()),

    url(r'^magazine/issue/(?P<volume_number>[\d\+]+)/$', name='issue-detail', view=IssueDetailView.as_view()),
)
