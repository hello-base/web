from django.conf.urls import patterns, url

from .views import (ShowListView, ShowDetailView, ShowCreateView, ShowUpdateView,
    EpisodeDetailView, EpisodeCreateView, EpisodeUpdateView, MagazineListView, MagazineDetailView,
    MagazineCreateView, MagazineUpdateView, IssueDetailView, IssueCreateView, IssueUpdateView)


urlpatterns = patterns('',

    url(r'^show/(?P<slug>[-\w]+)/$', name='show-detail', view=ShowDetailView.as_view()),
    url(r'^show/$', name='show-list', view=ShowListView.as_view()),

    url(r'^show/(?P<slug>[-\w]+)/(?P<year>d{4})-(?P<month>d{2})-(?P<day>d+)/$', name='episode-detail', view=EpisodeDetailView.as_view()),

    url(r'^magazine/(?P<slug>[-\w]+)/$', name='magazine-detail', view=MagazineDetailView.as_view()),
    url(r'^magazine/$', name='magazine-list', view=MagazineListView.as_view()),

    url(r'^magazine/issue/(?P<volume_number>[\d\+]+)/$', name='issue-detail', view=IssueDetailView.as_view()),

    url(r'^show/create/$', name='show-create', view=ShowCreateView.as_view()),
    url(r'^show/update/(?P<pk>\d+)/$', name='show-update', view=ShowUpdateView.as_view()),
    url(r'^show/episode/create/$', name='episode-create', view=ShowCreateView.as_view()),
    url(r'^show/episode/update/(?P<pk>\d+)/$', name='episode-update', view=ShowUpdateView.as_view()),
    url(r'^magazine/create/$', name='magazine-create', view=ShowCreateView.as_view()),
    url(r'^magazine/update/(?P<pk>\d+)/$', name='magazine-update', view=ShowUpdateView.as_view()),
    url(r'^magazine/issue/create/$', name='issue-create', view=ShowCreateView.as_view()),
    url(r'^magazine/issue/update/(?P<pk>\d+)/$', name='issue-update', view=ShowUpdateView.as_view()),
)
