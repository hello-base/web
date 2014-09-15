# -*- coding: utf-8 -*-
import calendar

from django import template
register = template.Library()

from base.apps.correlations.constants import FIELD_MAPPING


@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]


@register.simple_tag
def render_statistic_label(app_label, model_name, date_field):
    key = (app_label, model_name, date_field)
    return FIELD_MAPPING[key]
