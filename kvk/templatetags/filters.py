from typing import Dict
from django import template

register = template.Library()


@register.filter
def get(dic: Dict, key):
    return dic[key]
