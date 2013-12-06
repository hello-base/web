# -*- coding: utf-8 -*-
from collections import OrderedDict
from itertools import groupby

from django.views.generic.dates import YearArchiveView

from .models import Correlation


class HappeningsByYearView(YearArchiveView):
    allow_future = True
    date_field = 'timestamp'
    make_object_list = True
    queryset = Correlation.objects.all()
    template_name = 'correlations/happenings_year.html'

    def get_context_data(self, **kwargs):
        context = super(HappeningsByYearView, self).get_context_data(**kwargs)
        context['years'] = self.get_years()
        return context

    def get_years(self):
        decades = {}
        dqs = Correlation.objects.dates('timestamp', 'year').reverse()
        for key, group in groupby(dqs, lambda y: str(y.year)[:3]):
            key = '%s0s' % key
            decades[key] = list(year for year in group)
        return OrderedDict(sorted(decades.iteritems(), key=lambda y: y[0]))
