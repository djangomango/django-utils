from typing import Any

from django import template
from django.template import NodeList, Parser, Token
from django.template.base import FilterExpression
from django.template.context import Context
from django.template.loader import render_to_string

register = template.Library()


class RenderComponentNode(template.Node):
    """Template node for rendering component templates with dynamic context."""

    def __init__(
        self,
        template_name: str,
        context_args: dict[str, Any] | None,
        context_kwargs: dict[str, Any] | None,
        nodelist: NodeList,
    ) -> None:
        """Initialize render component node."""
        self.template_name = template_name
        self.context_args = context_args or {}
        self.context_kwargs = context_kwargs or {}
        self.nodelist = nodelist

    def render(self, context: Context) -> str:
        """Render component template with resolved context arguments and nested content."""
        resolved_context_args = {
            key: (value.resolve(context) if not isinstance(value, str) else value)
            for key, value in self.context_args.items()
            if value
        }
        resolved_context_kwargs = {
            key: (value.resolve(context) if not isinstance(value, str) else value)
            for key, value in self.context_kwargs.items()
            if value
        }
        content = self.nodelist.render(context)

        ctx = {"content": content, "attrs": resolved_context_kwargs}
        ctx.update(resolved_context_args)

        return render_to_string(self.template_name, ctx)


@register.tag
def render_component(
    parser: Parser,
    token: Token,
    template_name: str,
    context_args: dict[str, Any],
) -> RenderComponentNode:
    """Parse render_component template tag and return node instance."""
    tag_name = ""
    try:
        tag_name, *args = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            f"{tag_name} tag requires at least one argument."
        )

    context_kwargs: dict[str, FilterExpression | None] = {}

    for arg in args:
        try:
            name, value = arg.split("=")
            if name in context_args:
                context_args[name] = parser.compile_filter(value)
            else:
                context_kwargs[name] = parser.compile_filter(value)
        except ValueError:
            context_args[arg] = None

    nodelist = parser.parse((f"end_{tag_name}",))
    parser.delete_first_token()

    return RenderComponentNode(template_name, context_args, context_kwargs, nodelist)
