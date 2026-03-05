from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def convert_minutes_to_time(total_minutes):
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f'{hours}<span class="timer-dot">:</span>{minutes}<span class="timer-dot">:</span>00'