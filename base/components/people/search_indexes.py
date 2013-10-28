from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from .constants import SCOPE, STATUS
from .models import Group, Idol


class IdolIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    model = indexes.CharField(model_attr='_meta__verbose_name_plural', faceted=True)
    romanized_name = indexes.CharField(model_attr='romanized_name')
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Idol

    def index_queryset(self, using=None):
        qs = super(IdolIndex, self).index_queryset(using=using)
        qs = qs.select_related('primary_membership__group')
        return qs


class GroupIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    model = indexes.CharField(model_attr='_meta__verbose_name_plural', faceted=True)
    romanized_name = indexes.CharField(model_attr='romanized_name')
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Group

    def prepare(self, obj):
        data = super(GroupIndex, self).prepare(obj)
        data['boost'] = 1.0

        # Boost active groups, demote inactive groups.
        if obj.status == STATUS.active:
            data['boost'] += 0.1
        else:
            data['boost'] -= 0.1

        # Boost Hello! Project groups, demote non-H!P groups.
        if obj.scope == SCOPE.hp:
            data['boost'] += 0.1
        else:
            data['boost'] -= 0.1

        return data


# TODO: Staff won't be searchable until we actually make that data
# meaningful; with profile pages or something of that nature.
