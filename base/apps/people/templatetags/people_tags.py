# -*- coding: utf-8 -*-
from datetime import date

from django import template
register = template.Library()

from ..models import Group
from ..utils import calculate_age


@register.filter
def age(value, target=None):
    return calculate_age(value, target=target)


@register.simple_tag
def designation_for(target, target_date=date.today()):
    if isinstance(target, Group):
        return target.designation_for(target=target_date).name
    return target.name


@register.simple_tag
def romanized_designation_for(target, target_date=date.today()):
    if isinstance(target, Group):
        return target.designation_for(target=target_date).romanized_name
    return target.romanized_name
