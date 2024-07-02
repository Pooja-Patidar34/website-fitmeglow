# products/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='mul')
def mul(value, arg):
    try:
        value = float(value) if value else 0.0
        arg = float(arg) if arg else 0.0
        return value * arg
    except (ValueError, TypeError):
        return 0.0
