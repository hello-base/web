# -*- coding: utf-8 -*-
from django.views.generic.dates import DateDetailView, YearArchiveView

from .models import Item


class NewsIndexView(YearArchiveView):
    model = Item


class ItemDetailView(DateDetailView):
    model = Item
    date_field = 'published'
