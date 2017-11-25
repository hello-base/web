# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import AggregateJulianCorrelationView, HappeningsByYearView


urlpatterns = [
    url(r'^correlations/graphs/month/$', view=AggregateJulianCorrelationView.as_view(), name='correlations-aggregate-julian'),
    url(r'^happenings/(?P<year>\d{4})/$', view=HappeningsByYearView.as_view(), name='happenings-by-year')
]
