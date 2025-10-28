# -*- coding: utf-8 -*-
from django.urls import re_path

from .views import ItemDetailView, NewsIndexView


urlpatterns = [
    re_path(r'^news/(?P<year>\d{4})/(?P<month>[-\w]+)/(?P<slug>[-\w]+)/$', ItemDetailView.as_view(), name='item-detail'),
    re_path(r'^news/$', NewsIndexView.as_view(), name='news-index'),
]
