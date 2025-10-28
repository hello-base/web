from django.urls import re_path

from .views import GoodsBrowseView, ShopDetailView, ShopListView


urlpatterns = [
    re_path(r'^goods/$', GoodsBrowseView.as_view(), name='goods-browse'),

    re_path(r'^shop/(?P<slug>[-\w]+)/$', ShopDetailView.as_view(), name='shop-detail'),
    re_path(r'^shop/$', ShopListView.as_view(), name='shop-list'),
]
