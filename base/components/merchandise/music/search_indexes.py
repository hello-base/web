import datetime

from haystack import indexes

from .models import Album, Single


class AlbumIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    model = indexes.CharField(model_attr="_meta__verbose_name_plural", faceted=True)

    def get_model(self):
        return Album

    def index_queryset(self, using=None):
        qs = super(AlbumIndex, self).index_queryset(using=using)
        qs = qs.prefetch_related('participating_idols', 'participating_groups')
        return qs


class SingleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    model = indexes.CharField(model_attr="_meta__verbose_name_plural", faceted=True)

    def get_model(self):
        return Single

    def index_queryset(self, using=None):
        qs = super(SingleIndex, self).index_queryset(using=using)
        qs = qs.prefetch_related('participating_idols', 'participating_groups')
        return qs
