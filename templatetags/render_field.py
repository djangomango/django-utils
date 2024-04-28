from django import template
from django.template.loader import render_to_string

register = template.Library()


class RenderFieldNode(template.Node):

    def __init__(self, template_name, context_args):
        self.template_name = template_name
        self.context_args = context_args or {}

    def render(self, context):
        resolved_context_args = {
            key: (value.resolve(context) if not isinstance(value, str) else value)
            for key, value in self.context_args.items() if value
        }

        ctx = {'field': resolved_context_args.pop('field')}
        ctx.update(resolved_context_args)

        return render_to_string(self.template_name, ctx)


@register.tag
def render_field(parser, token, template_name):
    try:
        tag_name, *args = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(f"{tag_name} tag requires at least one argument.")

    context_args = {}

    for arg in args:
        try:
            name, value = arg.split('=')
            context_args[name] = parser.compile_filter(value)
        except ValueError:
            context_args[arg] = None

    return RenderFieldNode(template_name, context_args)
