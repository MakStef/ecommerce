from django import template

from store.utils import utils

import json

register = template.Library()


@register.simple_tag
def products_to_json(products, user):
    return json.dumps(utils.products_to_values_list(products))