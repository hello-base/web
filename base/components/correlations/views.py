# -*- coding: utf-8 -*-
from collections import defaultdict, OrderedDict
from itertools import groupby

from django.contrib.contenttypes.models import ContentType
from django.views.generic.dates import YearArchiveView

from components.people.models import Membership

from .constants import SUBJECTS
from .models import Correlation
from .utils import dictify


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

        # Because of the way generic relations work, the foreign keys of any
        # content object can't be prefetched. We'll manually prefetch what we
        # need for the Membership class and strap that to the existing queryset.
        generics = {}
        for item in correlations:
            generics.setdefault(item.content_type_id, set()).add(item.object_id)

        content_types = ContentType.objects.in_bulk(generics.keys())

        relations = {}
        for ct, fk_list in generics.items():
            ct_model = content_types[ct].model_class()
            if ct_model is Membership:
                relations[ct] = ct_model.objects.select_related('idol', 'group').in_bulk(list(fk_list))
            else:
                relations[ct] = ct_model.objects.in_bulk(list(fk_list))

        for item in correlations:
            setattr(item, '_content_object_cache', relations[item.content_type_id][item.object_id])

        objects = defaultdict(lambda: defaultdict(list))
        for c in correlations:
            objects[c.month][c.day].append(c)

        # Remove the defaultdict-ness from the objects. Then, sort the nested
        # dictionaries and then finally the main dictionary--all in reverse.
        objects = dictify(objects)
        for k, v in objects.iteritems():
            objects[k] = OrderedDict(sorted(v.iteritems(), reverse=True))
        return OrderedDict(sorted(objects.iteritems(), reverse=True))

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

    def get_average_statistics(self):
        pass
