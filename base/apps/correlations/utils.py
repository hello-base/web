# -*- coding: utf-8 -*-
from collections import defaultdict, OrderedDict

from django.contrib.contenttypes.models import ContentType

from base.apps.people.models import Membership
from base.apps.merchandise.music.models import Album, Single


def call_attributes(instance, attribute_list):
    for attribute in attribute_list:
        if hasattr(instance, attribute):
            return (getattr(instance, attribute), attribute)
    raise AttributeError


def dictify(d):
    return {k: dictify(v) for k, v in d.items()} if isinstance(d, defaultdict) else d


def prefetch_relations(queryset):
    # Because of the way generic relations work, the foreign keys of any
    # content object can't be prefetched. We'll manually prefetch what we
    # need for the Membership class and strap that to the existing queryset.
    generics = {}
    [generics.setdefault(item.content_type_id, set()).add(item.object_id) for item in queryset]

    relations = {}
    content_types = ContentType.objects.in_bulk(generics.keys())
    for ct, fk_list in generics.items():
        ct_model = content_types[ct].model_class()
        if ct_model is Membership:
            relations[ct] = ct_model.objects.select_related('idol', 'group').in_bulk(list(fk_list))
        elif ct_model in [Album, Single]:
            relations[ct] = ct_model.objects.prefetch_related('participating_idols', 'participating_groups').in_bulk(list(fk_list))
        else:
            relations[ct] = ct_model.objects.in_bulk(list(fk_list))

    [setattr(item, '_content_object_cache', relations[item.content_type_id][item.object_id]) for item in queryset]
    return queryset


def regroup_correlations(queryset):
    objects = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for c in queryset:
        objects[c.year][c.month][c.day].append(c)

    # Remove the defaultdict-ness from the objects. Then, sort the nested
    # dictionaries and then finally the main dictionary--all in reverse.
    objects = dictify(objects)
    for k, v in objects.iteritems():
        objects[k] = OrderedDict(sorted(v.iteritems(), reverse=True))
    return OrderedDict(sorted(objects.iteritems(), reverse=True))


def regroup_yearly_correlations(queryset):
    objects = defaultdict(lambda: defaultdict(list))
    for c in queryset:
        objects[c.month][c.day].append(c)

    # Remove the defaultdict-ness from the objects. Then, sort the nested
    # dictionaries and then finally the main dictionary--all in reverse.
    objects = dictify(objects)
    for k, v in objects.iteritems():
        objects[k] = OrderedDict(sorted(v.iteritems(), reverse=True))
    return OrderedDict(sorted(objects.iteritems(), reverse=True))
