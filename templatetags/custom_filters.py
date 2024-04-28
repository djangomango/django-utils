import decimal
import requests
from apps.utils.helpers.dict import get_dict_item_or_default, string_to_dict_or_default
from apps.utils.helpers.string import get_short_email, get_short_url, get_short_number
from datetime import date, datetime
from django import template
from django.core.files.storage import default_storage
from django.db import models

from ..helpers.requests import get_agent_head_or_default

register = template.Library()


@register.filter
def to_dict(value):
    return string_to_dict_or_default(value, None)


@register.filter
def get_dict_item(dictionary, key):
    return get_dict_item_or_default(dictionary, key, None)


@register.filter
def starts_with(string, starts):
    if isinstance(string, str) and isinstance(starts, str):
        return string.endswith(starts)

    return False


@register.filter
def ends_with(string, ends):
    if isinstance(string, str) and isinstance(ends, str):
        return string.endswith(ends)

    return False


@register.filter
def remove_substr(string, substr):
    if isinstance(string, str) and isinstance(substr, str):
        return string.replace(substr, '')

    return string


@register.simple_tag
def replace_substr(string, substr, newstr):
    if isinstance(string, str) and isinstance(substr, str):
        return string.replace(substr, newstr)

    return string


@register.filter
def short_email(string):
    if isinstance(string, str):
        return get_short_email(string)

    return string


@register.filter
def short_url(string):
    if isinstance(string, str):
        return get_short_url(string)

    return string


@register.filter
def short_number(value):
    if isinstance(value, (int, float, decimal.Decimal)):
        return get_short_number(value)

    return value


@register.filter(expects_localtime=True)
def days_since(dt):
    if isinstance(dt, date):
        tzinfo = getattr(dt, 'tzinfo', None)
        day = date(dt.year, dt.month, dt.day)
        today = datetime.now(tzinfo).date()
        delta = day - today
        return abs(delta.days)

    return dt


@register.filter
def divide(value, divisor):
    if all(isinstance(i, (int, float, decimal.Decimal)) for i in [value, divisor]):
        return float(value) / float(divisor)

    return value


@register.filter
def file_exists(file):
    if isinstance(file, models.FileField):
        return default_storage.exists(file.path)

    return False


@register.filter
def url_exists(url):
    if isinstance(url, str):
        head = get_agent_head_or_default()
        req = requests.get(url, headers=head, timeout=2)
        return req.status_code == requests.codes.ok

    return False
