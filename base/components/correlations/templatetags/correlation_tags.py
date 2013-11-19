# -*- coding: utf-8 -*-
from django import template
register = template.Library()


@register.inclusion_tag('correlations/partials/historic_correlation.html')
def render_correlation(instance):
    return {
        'field': instance.date_field,
        'identifier': instance.identifier,
        'object': instance.content_object,
        'timestamp': instance.timestamp
    }
