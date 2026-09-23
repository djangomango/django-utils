from typing import Any

from django import forms


class ButtonHolderMixin:
    """A mixin for Django form classes that allows setting a button for the form."""

    button = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.button is not None:
            self.fields["submit"] = forms.CharField(
                widget=forms.HiddenInput(), initial=self.button
            )

    def render_button(self) -> str:
        """Render HTML submit button markup."""
        return f'<button type="submit">{self.button}</button>'
