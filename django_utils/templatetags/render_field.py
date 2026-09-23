from typing import Any

from django import template
from django.template import Parser, Token
from django.template.base import FilterExpression
from django.template.context import Context
from django.template.loader import render_to_string

register = template.Library()


class RenderFieldNode(template.Node):
    """Template node for rendering form field templates with custom context."""

    def __init__(
        self,
        template_name: str,
        context_args: dict[str, Any] | None,
    ) -> None:
        """Initialize render field node."""
        self.template_name = template_name
        self.context_args = context_args or {}

    def render(self, context: Context) -> str:
        """Render field template with resolved context arguments."""
        resolved_context_args = {
            key: (value.resolve(context) if not isinstance(value, str) else value)
            for key, value in self.context_args.items()
            if value
        }

        ctx = {"field": resolved_context_args.pop("field")}
        ctx.update(resolved_context_args)

        return render_to_string(self.template_name, ctx)


@register.tag
def render_field(
    parser: Parser,
    token: Token,
    template_name: str,
) -> RenderFieldNode:
    """Parse render_field template tag and return node instance."""
    tag_name = ""
    try:
        tag_name, *args = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            f"{tag_name} tag requires at least one argument."
        )

    context_args: dict[str, FilterExpression | None] = {}

    for arg in args:
        try:
            name, value = arg.split("=")
            context_args[name] = parser.compile_filter(value)
        except ValueError:
            context_args[arg] = None

    return RenderFieldNode(template_name, context_args)
