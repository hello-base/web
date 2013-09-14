from django import template
register = template.Library()

from ..utils import calculate_age


@register.filter
def age(value, target):
    return calculate_age(value, target=target)
