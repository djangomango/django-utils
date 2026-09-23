import re
from typing import Any

from django import template
from django.template import Node
from django.utils.encoding import force_str

register = template.Library()


def strip_spaces_in_tags(value: Any) -> str:
    """Strip extraneous whitespace between HTML tags."""
    value = force_str(value)
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r">\s+", ">", value)
    value = re.sub(r"\s+<", "<", value)
    return str(value)


class NoSpacesNode(Node):
    """Template node that collapses whitespace between HTML tags in rendered output."""

    def __init__(self, nodelist: Any) -> None:
        self.nodelist = nodelist

    def render(self, context: Any) -> str:
        return strip_spaces_in_tags(self.nodelist.render(context).strip())


@register.tag
def all_spaceless(parser: Any, token: Any) -> NoSpacesNode:
    """Template tag compiler removing whitespace between HTML elements."""
    nodelist = parser.parse(("end_all_spaceless",))
    parser.delete_first_token()
    return NoSpacesNode(nodelist)
