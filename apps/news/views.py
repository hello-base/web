# -*- coding: utf-8 -*-
from django.views.generic import DetailView
from django.views.generic.dates import ArchiveIndexView

from .models import Item


class NewsIndexView(ArchiveIndexView):
    model = Item
    date_field = 'published'


class ItemDetailView(DetailView):
    model = Item
    date_field = 'published'
