from django.conf.urls import patterns, url

from .views import (GoodsBrowseView, ShopListView, ShopDetailView, 
    ShopCreateView, ShopUpdateView, GoodCreateView, GoodUpdateView, 
    SetCreateView, SetUpdateView, SuperSetCreateView, SuperSetUpdateView)


urlpatterns = patterns('',
    url(r'^goods/$', name='goods-browse', view=GoodsBrowseView.as_view()),
    
    url(r'^shop/(?P<slug>[-\w]+)/$', name='shop-detail', view=ShopDetailView.as_view()),
    url(r'^shop/$', name='shop-list', view=ShopListView.as_view()),
    
    url(r'^shop/create/$', name='shop-create', view=ShopCreateView.as_view()),
    url(r'^shop/update/(?P<pk>\d+)/$', name='shop-update', view=ShopUpdateView.as_view()),
    url(r'^good/create/$', name='good-create', view=GoodCreateView.as_view()),
    url(r'^good/update/(?P<pk>\d+)/$', name='good-update', view=GoodUpdateView.as_view()),
    url(r'^set/create/$', name='set-create', view=SetCreateView.as_view()),
    url(r'^set/update/(?P<pk>\d+)/$', name='set-update', view=SetUpdateView.as_view()),
    url(r'^superset/create/$', name='superset-create', view=SuperSetCreateView.as_view()),
    url(r'^superset/update/(?P<pk>\d+)/$', name='superset-update', view=SuperSetUpdateView.as_view()),
)