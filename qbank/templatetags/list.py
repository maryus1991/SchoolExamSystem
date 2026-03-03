from django import template

register = template.Library()


@register.filter
def list_index(list, id):
    try:
        return list[id]
    except Exception as E:
        return 0
 