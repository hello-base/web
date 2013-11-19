# -*- coding: utf-8 -*-
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
        context['years'] = Correlation.objects.dates('timestamp', 'year')
        return context
