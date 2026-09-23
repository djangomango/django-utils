# Adapted from django-regex-field
# https://github.com/ambitioninc/django-regex-field
# version 3.0.3

import re
from typing import Any

from django.core.exceptions import ValidationError
from django.db import models


class CastOnAssignDescriptor:
    """Attribute descriptor that casts assigned values to Python via field."""

    def __init__(self, field: Any) -> None:
        self.field = field

    def __get__(self, obj: Any, type: type | None = None) -> Any:
        if obj is None:
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj: Any, value: Any) -> None:
        obj.__dict__[self.field.name] = self.field.to_python(value)


class RegexField(models.CharField):
    """Model field storing regular expression strings with compiled regex caching."""

    description = "A regular expression"
    compiled_regex_cache: dict[str, Any] = {}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.re_flags = kwargs.pop("re_flags", None)
        super().__init__(*args, **kwargs)

    def get_db_prep_value(
        self, value: Any, connection: Any, prepared: bool = False
    ) -> Any:
        value = self.to_python(value)
        return self.value_to_string(value)

    def get_cache_key(self, value: Any, flags: Any) -> str:
        """Generate cache key for compiled regular expression with flags."""
        return f"value-{value}-flags-{flags}"

    def get_compiled_regex(self, value: Any) -> re.Pattern[str]:
        """Return compiled regex pattern from cache or compile and store it."""
        cache_key = self.get_cache_key(value, self.re_flags)
        if cache_key not in self.compiled_regex_cache:
            if self.re_flags is None:
                self.compiled_regex_cache[cache_key] = re.compile(value)
            else:
                self.compiled_regex_cache[cache_key] = re.compile(
                    value, flags=self.re_flags
                )

        return self.compiled_regex_cache[cache_key]

    def from_db_value(
        self, value: Any, expression: Any, connection: Any, *args: Any
    ) -> Any:
        return self.to_python(value)

    def contribute_to_class(
        self, cls: type, name: str, virtual_only: bool = False
    ) -> None:
        super().contribute_to_class(cls, name, virtual_only)
        setattr(cls, name, CastOnAssignDescriptor(self))

    def to_python(self, value: Any) -> re.Pattern[str] | None:
        if isinstance(value, type(re.compile(""))):
            return value

        if value is None and self.null:
            return None

        try:
            return self.get_compiled_regex(value)
        except Exception:
            raise ValidationError(f"Invalid regex {value}")

    def value_to_string(self, obj: Any) -> str | None:
        if obj is None:
            return None

        if issubclass(obj.__class__, models.Model):
            obj = self.value_from_object(obj)

        pattern_type = re.Pattern
        if isinstance(obj, pattern_type):
            return obj.pattern

        return None

    def run_validators(self, value: Any) -> None:
        value = self.to_python(value)
        value = self.value_to_string(value)
        super().run_validators(value)
