# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import ItemDetailView, NewsIndexView


urlpatterns = [
    url(r'^news/(?P<year>\d{4})/(?P<month>[-\w]+)/(?P<slug>[-\w]+)/$', view=ItemDetailView.as_view(), name='item-detail'),
    url(r'^news/$', view=NewsIndexView.as_view(), name='news-index'),
]
