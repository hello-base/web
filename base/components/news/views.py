# -*- coding: utf-8 -*-
from django.views.generic.dates import ArchiveIndexView, DateDetailView

from .models import Item


class NewsIndexView(ArchiveIndexView):
    model = Item
    date_field = 'published'


class ItemDetailView(DateDetailView):
    model = Item
    date_field = 'published'
