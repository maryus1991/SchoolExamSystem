from django import template

register = template.Library()

@register.filter
def tdc(value: int):
    if value is not None and value and value != "":
        return "{:,}".format(int(value))
    else:
        return 0

@register.filter
def percent(current: int, max_num:int):
    try:
        return int((current / max_num)*100)
    except Exception as E :
        return 100
    