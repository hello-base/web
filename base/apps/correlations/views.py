# -*- coding: utf-8 -*-
from collections import defaultdict, OrderedDict
from itertools import groupby

from django.views.generic.dates import YearArchiveView
from django.views.generic import DetailView

from braces.views import JSONResponseMixin
from pandas import DataFrame

from .constants import SUBJECTS
from .models import Correlation
from .utils import (dictify, prefetch_relations, regroup_correlations,
    regroup_yearly_correlations)


class HappeningsByYearView(YearArchiveView):
    allow_future = True
    date_field = 'timestamp'
    make_object_list = True
    queryset = Correlation.objects.all()
    template_name = 'correlations/happenings_year.html'

    def get_context_data(self, **kwargs):
        context = super(HappeningsByYearView, self).get_context_data(**kwargs)
        context['objects'] = self.get_objects()
        context['years'] = self.get_years()

        # Only show statistics from 1997 on.
        if self.get_year() >= '1997':
            context['statistics'] = self.get_statistics()
        return context

    def get_objects(self):
        correlations = self.queryset.filter(year=self.get_year()).order_by('object_id')
        return regroup_yearly_correlations(prefetch_relations(correlations))

    def get_years(self):
        decades = {}
        dqs = Correlation.objects.dates('timestamp', 'year').reverse()
        for key, group in groupby(dqs, lambda y: str(y.year)[:3]):
            key = '%s0s' % key
            decades[key] = list(year for year in group)
        return OrderedDict(sorted(decades.iteritems(), key=lambda t: t[0]))

    def get_statistics(self):
        statistics = defaultdict(lambda: defaultdict(dict))
        correlations = Correlation.objects.filter(year=self.get_year())
        previous_correlations = Correlation.objects.filter(year=int(self.get_year()) - 1)

        # `identifiers` consists of tuples with the following signature:
        # "(subject app label, subject model name, subject date field)"
        identifiers = ((s[0]._meta.app_label, s[0]._meta.model_name, s[1]) for s in SUBJECTS)
        for i in identifiers:
            statistic = len([c for c in correlations if c.identifier == i[1] and c.date_field == i[2]])
            previous = len([c for c in previous_correlations if c.identifier == i[1] and c.date_field == i[2]])
            statistics[i[0]][i[1]][i[2]] = (statistic, statistic - previous)
        return OrderedDict(sorted(dictify(statistics).iteritems(), key=lambda t: t[0], reverse=True))


class AggregateJulianCorrelationView(JSONResponseMixin, DetailView):
    def get(self, request, *args, **kwargs):
        correlations = Correlation.objects.all().values('identifier', 'julian').reverse()
        frame = DataFrame.from_records(correlations, index='julian')
        frame = frame.groupby(lambda x: x).aggregate(lambda x: len(x))
        context = frame.reset_index().T.to_dict().values()
        return self.render_json_response(context)
