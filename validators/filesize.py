from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileSizeValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        max_size = round(self.max_size / 1048576, 1)
        value_size = round(value.size / 1048576, 1)

        if value.size > self.max_size:
            raise ValidationError(
                _(f'File size must be less than {max_size} MB. Your file is {value_size} MB.'), code='file-size'
            )