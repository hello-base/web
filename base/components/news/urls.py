# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import NewsIndexView


urlpatterns = patterns('',
    url(r'^news/$', view=NewsIndexView.as_view(), name='news-index'),
)
