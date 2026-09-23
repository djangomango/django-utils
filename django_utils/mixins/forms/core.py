from typing import Any

from django import forms


class PlaceholderMixin:
    """A mixin for Django form classes that allows setting placeholder text for form fields."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["placeholder"] = self.fields[field].label


class DisableFieldsMixin:
    """A mixin for Django form classes that allows disabling of form fields."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["disabled"] = True


class RequiredFieldsMixin:
    """A mixin for Django form classes that allows setting all fields as required."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True


class ReadOnlyFieldsMixin:
    """A mixin for Django form classes that allows setting all fields as read-only."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["readonly"] = True


class ReadOnlyFormMixin:
    """A mixin for Django form classes that allows setting all fields as read-only."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["readonly"] = True
        self.fields["csrfmiddlewaretoken"].widget.attrs["readonly"] = False


class ValidateRequiredFieldsMixin(forms.Form):
    """
    A mixin for Django form classes that allows disabling of required field validation.

    When `validate_required_fields` is set to `True` (the default), all required fields will be validated.
    When `validate_required_fields` is set to `False`, all required fields will not be validated.

    To use this mixin, simply subclass it and include it as a mixin in your form class.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.validate_required_fields = kwargs.pop("validate_required_fields", True)
        super().__init__(*args, **kwargs)

        if not self.validate_required_fields:
            for field in self.fields:
                if self.fields[field].required:
                    self.fields[field].required = False


class AutoCompleteMixin:
    """A mixin for Django form classes that allows disabling of autocomplete for form fields."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["autocomplete"] = "off"


class CustomErrorMessagesMixin:
    """A mixin for Django form classes that allows setting custom error messages for form fields."""

    error_messages = {}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field in self.error_messages:
                self.fields[field].error_messages.update(self.error_messages[field])
