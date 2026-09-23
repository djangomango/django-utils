from typing import Any

from django import template
from django.template import (
    Template,
    TemplateSyntaxError,
    Variable,
    VariableDoesNotExist,
)

register = template.Library()


class RenderTemplateNode(template.Node):
    """Template node that resolves variable content and renders it as inline Django template."""

    def __init__(self, content: str) -> None:
        self.content = Variable(content)

    def render(self, context: Any) -> str:
        try:
            resolved_content = self.content.resolve(context)
            return str(Template(resolved_content).render(context))
        except (VariableDoesNotExist, TemplateSyntaxError):
            return ""


@register.tag
def render_template(parser: Any, token: Any) -> RenderTemplateNode:
    """Template tag compiler parsing dynamic string content into RenderTemplateNode."""
    try:
        _tag_name, value = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(
            f"{token.contents.split()[0]!r} tag requires exactly one argument"
        )

    return RenderTemplateNode(value)
