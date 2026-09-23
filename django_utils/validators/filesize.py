from typing import Any

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileSizeValidator:
    """Validator ensuring uploaded file size does not exceed specified byte limit."""

    def __init__(self, size: int) -> None:
        self.size = size

    def __call__(self, value: Any) -> None:
        img_mb = round(value.size / 1048576, 1)
        max_mb = round(self.size / 1048576, 1)

        if value.size > self.size:
            raise ValidationError(
                _(
                    f"File size must be less than {max_mb} mb. Your file is {img_mb} mb."
                ),
                code="file-size",
            )
