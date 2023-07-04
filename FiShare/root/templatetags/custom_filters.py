import os
from django import template

register = template.Library()

@register.filter
def basename(value):
    if isinstance(value, str):
        return os.path.basename(value)
    elif hasattr(value, 'name'):  # Check if it's a FieldFile object
        return os.path.basename(value.name)
    return value
