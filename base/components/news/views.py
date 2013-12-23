# -*- coding: utf-8 -*-
from django.views.generic.dates import DateDetailView, YearArchiveView


class NewsIndexView(YearArchiveView):
    pass


class ItemDetailView(DateDetailView):
    pass
