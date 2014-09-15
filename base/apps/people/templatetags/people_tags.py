from django import template
register = template.Library()

from ..utils import calculate_age


@register.filter
def age(value, target=None):
    return calculate_age(value, target=target)
