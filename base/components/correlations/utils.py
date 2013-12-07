# -*- coding: utf-8 -*-
from collections import defaultdict


def call_attributes(instance, attribute_list):
    for attribute in attribute_list:
        if hasattr(instance, attribute):
            return (getattr(instance, attribute), attribute)
    raise AttributeError


def dictify(d):
    return {k: dictify(v) for k, v in d.items()} if isinstance(d, defaultdict) else d
