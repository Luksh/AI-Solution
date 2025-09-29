from django import template
import calendar

register = template.Library()

@register.filter
def month_name(value, month_number):
    """
    Convert a month number to its name.
    Usage: {{ value|month_name:month_number }}
    """
    try:
        month_num = int(month_number)
        if 1 <= month_num <= 12:
            return calendar.month_name[month_num]
        return month_number
    except (ValueError, TypeError):
        return month_number

@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary using the key.
    Usage: {{ dictionary|get_item:key }}
    """
    return dictionary.get(key)
