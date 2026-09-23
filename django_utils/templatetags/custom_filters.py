import decimal
import re
from datetime import date, datetime
from typing import Any

import requests
from django import template
from django.core.files.storage import default_storage
from django.db import models

from ..helpers.requests import get_agent_head_or_default

register = template.Library()


@register.filter
def get_item(dictionary: Any, key: Any) -> Any:
    """Return dictionary item by key if key is a primitive scalar."""
    if isinstance(dictionary, dict) and isinstance(key, (int, str, float, bool)):
        return dictionary.get(key)

    return dictionary


@register.filter
def starts_with(string: Any, starts: Any) -> Any:
    """Return True if string starts with prefix."""
    if isinstance(string, str) and isinstance(starts, str):
        return string.startswith(starts)

    return string


@register.filter
def ends_with(string: Any, ends: Any) -> Any:
    """Return True if string ends with suffix."""
    if isinstance(string, str) and isinstance(ends, str):
        return string.endswith(ends)

    return string


@register.filter
def remove_substr(string: Any, substr: Any) -> Any:
    """Remove all occurrences of substring from string."""
    if isinstance(string, str) and isinstance(substr, str):
        string = string.replace(substr, "")

    return string


@register.simple_tag
def replace_substr(string: Any, substr: Any, newstr: Any) -> Any:
    """Replace occurrences of substring with replacement string."""
    if all(isinstance(i, str) for i in [string, substr, newstr]):
        string = string.replace(substr, newstr)

    return string


@register.filter
def short_email(string: Any) -> Any:
    """Strip local part of email, returning only domain portion."""
    if isinstance(string, str) and "@" in string:
        string = string[string.index("@") :]

    return string


@register.filter
def short_url(string: Any) -> Any:
    """Strip protocol, www prefix, and trailing slash from URL string."""
    if isinstance(string, str):
        if string.startswith("http"):
            string = re.sub(r"https?://", "", string)
        if string.startswith("www."):
            string = re.sub(r"www.", "", string)
        if string.endswith("/"):
            string = string[:-1]

    return string


@register.filter
def short_number(value: Any) -> Any:
    """Format large numbers into compact k/M abbreviations."""
    if isinstance(value, (int, float, decimal.Decimal)):
        value_int = int(value)
        if value_int > 1000000:
            value = f"{value_int / 1000000:.0f}M"
        elif value_int > 1000:
            value = f"{value_int / 1000:.0f}k"

    return value


@register.filter(expects_localtime=True)
def days_since(dt: Any) -> Any:
    """Calculate absolute number of days elapsed since date."""
    if isinstance(dt, date):
        tzinfo = getattr(dt, "tzinfo", None)
        day = date(dt.year, dt.month, dt.day)
        today = datetime.now(tzinfo).date()
        delta = day - today
        return abs(delta.days)

    return dt


@register.filter
def divide(value: Any, divisor: Any) -> Any:
    """Divide value by divisor as floating-point division."""
    if all(isinstance(i, (int, float, decimal.Decimal)) for i in [value, divisor]):
        return float(value) / float(divisor)

    return value


@register.filter
def file_exists(file: Any) -> bool:
    """Return True if model file field exists in default storage."""
    if isinstance(file, models.FileField):
        return default_storage.exists(file.path)

    return False


@register.filter
def url_exists(url: Any) -> bool:
    """Check if external URL responds with HTTP 200."""
    if isinstance(url, str):
        head = get_agent_head_or_default()
        req = requests.get(url, headers=head, timeout=2)
        return req.status_code == requests.codes.ok

    return False
