import datetime

from haystack import indexes

from .models import Group, Idol


class IdolIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)

    def get_model(self):
        return Idol


class GroupIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)

    def get_model(self):
        return Group


# TODO: Staff won't be searchable until we actually make that data
# meaningful; with profile pages or something of that nature.
