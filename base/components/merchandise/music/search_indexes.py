import datetime

from haystack import indexes

from .models import Album, Single


class AlbumIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    model = indexes.CharField(model_attr="_meta__verbose_name_plural", faceted=True)

    def get_model(self):
        return Album


class SingleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    model = indexes.CharField(model_attr="_meta__verbose_name_plural", faceted=True)

    def get_model(self):
        return Single
