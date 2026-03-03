from django import template

register = template.Library()

@register.filter
def tdc(value: int):
    if value is not None and value and value != "":
        return "{:,}".format(int(value))
    else:
        return 0