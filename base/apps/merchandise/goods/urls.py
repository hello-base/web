from django.conf.urls import patterns, url

from .views import GoodsBrowseView, ShopDetailView, ShopListView


urlpatterns = patterns('',
    url(r'^goods/$', name='goods-browse', view=GoodsBrowseView.as_view()),

    url(r'^shop/(?P<slug>[-\w]+)/$', name='shop-detail', view=ShopDetailView.as_view()),
    url(r'^shop/$', name='shop-list', view=ShopListView.as_view()),
)
