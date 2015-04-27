# -*- coding: utf-8 -*-
from haystack import indexes

from .models import Album, Single


class ReleaseIndex(indexes.SearchIndex):
    text = indexes.NgramField(document=True, use_template=True)
    model = indexes.CharField(model_attr='_meta__verbose_name_plural', faceted=True)
    romanized_name = indexes.CharField(model_attr='romanized_name')
    name = indexes.CharField(model_attr='name')

    class Meta:
        abstract = True

    def index_queryset(self, using=None):
        qs = super(ReleaseIndex, self).index_queryset(using=using)
        qs = qs.prefetch_related('participating_idols', 'participating_groups')
        return qs


class AlbumIndex(ReleaseIndex, indexes.Indexable):
    def get_model(self):
        return Album


class SingleIndex(ReleaseIndex, indexes.Indexable):
    def get_model(self):
        return Single
