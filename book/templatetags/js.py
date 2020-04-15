from django.utils.safestring import mark_safe
from django.template import Library
import itertools

import json

register = Library()


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))


@register.filter(is_safe=True)
def class_like(string):
    new_string = str(string).replace(" ", "-").replace("(", "").replace(")", "")\
                            .replace(",", "").replace('"', "").replace(".", "")\
                            .replace("?", "").replace("!", "").replace('"', "")
    return mark_safe(new_string)


@register.filter(is_safe=True)
def book_set_to_json(query_set):
    # converts the book model into a json model, so i can use it in javascript
    full_dict = {}
    counter = 0
    for item in query_set:

        full_dict[counter] = {
            'book_name': item.book_name,
            'book_author': item.book_author,
            'slug': item.slug,
            'book_id': item.id,
        }
        counter += 1

    r = json.dumps(full_dict)
    return json.loads(r)

