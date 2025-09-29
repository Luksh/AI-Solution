from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Split a string by the specified delimiter and return a list.
    Usage: {{ value|split:'delimiter' }}
    Example: {{ features|split:',' }}
    """
    return [item.strip() for item in value.split(arg)]
