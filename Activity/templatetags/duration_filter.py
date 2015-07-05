# coding=utf-8
from django.template import Library

register = Library()


@register.filter(name="duration")
def duration(minutes):
    m = minutes % 60
    h = int(minutes / 60)
    d = int(h/24)
    h -= d*2
    if h > 0:
        description = "%sd%sh%sm" % (d, h, m)
    elif d > 0:
        description = "%sh%sm" % (h, m)
    else:
        description = "%sm" % m
    return description