from typing import Any

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class MimeTypeValidator:
    """Validator verifying uploaded file MIME type against allowed list using libmagic or standard mimetypes."""

    def __init__(
        self, mimetypes: Any, message: str | None = None, code: str = "file-type"
    ) -> None:
        self.mimetypes = mimetypes
        self.message = message
        self.code = code

    def __call__(self, value: Any) -> None:
        try:
            import magic

            mime = magic.from_buffer(value.read(2048), mime=True)
        except (ImportError, Exception):
            import mimetypes

            mime, _ = mimetypes.guess_type(getattr(value, "name", ""))

        if mime != "application/octet-stream" and mime not in self.mimetypes:
            if not self.message:
                raise ValidationError(
                    _(f"{value} is not an acceptable file type."), code=self.code
                )
            else:
                raise ValidationError(_(self.message), code=self.code)
