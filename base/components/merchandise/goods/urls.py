from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^goods/$', name='goods-browse', view=views.GoodsBrowseView.as_view()),

    url(r'^shop/(?P<slug>[-\w]+)/$', name='shop-detail', view=views.ShopDetailView.as_view()),
    url(r'^shop/$', name='shop-list', view=views.ShopListView.as_view()),
    url(r'^shop/create/$', name='shop-create', view=views.ShopCreateView.as_view()),
    url(r'^shop/update/(?P<pk>\d+)/$', name='shop-update', view=views.ShopUpdateView.as_view()),

    url(r'^good/create/$', name='good-create', view=views.GoodCreateView.as_view()),
    url(r'^good/update/(?P<pk>\d+)/$', name='good-update', view=views.GoodUpdateView.as_view()),
    url(r'^set/create/$', name='set-create', view=views.SetCreateView.as_view()),
    url(r'^set/update/(?P<pk>\d+)/$', name='set-update', view=views.SetUpdateView.as_view()),
    url(r'^superset/create/$', name='superset-create', view=views.SuperSetCreateView.as_view()),
    url(r'^superset/update/(?P<pk>\d+)/$', name='superset-update', view=views.SuperSetUpdateView.as_view()),
)
