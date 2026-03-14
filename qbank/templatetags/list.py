from django import template

register = template.Library()


@register.filter
def list_index(lis, id):
    lis = list(lis)
    try:
        return lis[id]
    except Exception as E:
        return 0
 

 