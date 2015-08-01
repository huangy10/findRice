# coding=utf-8
import datetime
from django.template import Library
from django.utils import timezone
register = Library()


@register.filter(name="duration")
def duration(minutes):
    m = minutes % 60
    h = int(minutes / 60)
    d = int(h/24)
    h -= d*24
    if h > 0:
        description = "%sd%sh" % (d, h)
    elif d > 0:
        description = "%sh%sm" % (h, m)
    else:
        description = "%sm" % m
    return description


@register.filter(name="two_line")
def two_line(content):
    text = content.split("\n")
    return text[0:2]


@register.filter(name="seperate_to_p")
def seperate_to_p(content):
    return content.split("\n")


@register.filter(name="datefilter")
def datefilter(date):
    return date.strftime("%Y-%m-%d")


@register.filter(name='datetime_filter')
def datetime_filter(date):
    tz = timezone.get_current_timezone()
    return tz.normalize(date).strftime("%Y-%m-%d %H:%m")
