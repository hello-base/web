# -*- coding: utf-8 -*-
from django.urls import re_path

from .views import AggregateJulianCorrelationView, HappeningsByYearView


urlpatterns = [
    re_path(r'^correlations/graphs/month/$', AggregateJulianCorrelationView.as_view(), name='correlations-aggregate-julian'),
    re_path(r'^happenings/(?P<year>\d{4})/$', HappeningsByYearView.as_view(), name='happenings-by-year')
]
