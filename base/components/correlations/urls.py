# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import HappeningsByYearView


urlpatterns = patterns('',
    url(r'^happenings/(?P<year>\d{4})/$', view=HappeningsByYearView.as_view(), name='happenings-by-year')
)
