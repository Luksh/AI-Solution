from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary using the key.
    Usage: {{ dictionary|get_item:key }}
    """
    return dictionary.get(key)

@register.filter
def get_category_display(category_code):
    """
    Convert a category code to its display name.
    Usage: {{ category_code|get_category_display }}
    """
    category_mapping = {
        'ai_technology': 'AI Technology',
        'machine_learning': 'Machine Learning',
        'data_science': 'Data Science',
        'business_intelligence': 'Business Intelligence',
        'industry_insights': 'Industry Insights',
        'case_studies': 'Case Studies',
        'company_news': 'Company News',
    }
    return category_mapping.get(category_code, category_code)

@register.filter
def filter_by_category(queryset, category):
    """
    Filter a queryset by category.
    Usage: {{ queryset|filter_by_category:category }}
    """
    from django.core.paginator import Page
    
    # If it's a Page object from pagination, get the object_list
    if isinstance(queryset, Page):
        queryset = queryset.object_list
    
    # Filter the queryset
    from django.db.models import QuerySet
    if isinstance(queryset, QuerySet):
        return queryset.filter(category=category)
    else:
        return [item for item in queryset if item.category == category]

@register.filter
def divide(value, arg):
    """
    Divide the value by the argument.
    Usage: {{ value|divide:arg }}
    """
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0
