import datetime

from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from .models import Group, Idol


class IdolIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    model = indexes.CharField(model_attr="_meta__verbose_name_plural", faceted=True)

    def get_model(self):
        return Idol

    def index_queryset(self, using=None):
        qs = super(IdolIndex, self).index_queryset(using=using)
        qs = qs.select_related('primary_membership__group')
        return qs


class GroupIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    model = indexes.CharField(model_attr="_meta__verbose_name_plural", faceted=True)

    def get_model(self):
        return Group


# TODO: Staff won't be searchable until we actually make that data
# meaningful; with profile pages or something of that nature.
