from django import template
from django.template.loader import render_to_string

register = template.Library()


class RenderComponentNode(template.Node):

    def __init__(self, template_name, context_args, context_kwargs, nodelist):
        self.template_name = template_name
        self.context_args = context_args or {}
        self.context_kwargs = context_kwargs or {}
        self.nodelist = nodelist

    def render(self, context):
        resolved_context_args = {
            key: (value.resolve(context) if not isinstance(value, str) else value)
            for key, value in self.context_args.items() if value
        }
        resolved_context_kwargs = {
            key: (value.resolve(context) if not isinstance(value, str) else value)
            for key, value in self.context_kwargs.items() if value
        }
        content = self.nodelist.render(context)

        ctx = {'content': content, 'attrs': resolved_context_kwargs}
        ctx.update(resolved_context_args)

        return render_to_string(self.template_name, ctx)


@register.tag
def render_component(parser, token, template_name, context_args):
    try:
        tag_name, *args = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(f"{tag_name} tag requires at least one argument.")

    context_kwargs = {}

    for arg in args:
        try:
            name, value = arg.split('=')
            if name in context_args.keys():
                context_args[name] = parser.compile_filter(value)
            else:
                context_kwargs[name] = parser.compile_filter(value)
        except ValueError:
            context_args[arg] = None

    nodelist = parser.parse(('end_' + tag_name,))
    parser.delete_first_token()

    return RenderComponentNode(template_name, context_args, context_kwargs, nodelist)
