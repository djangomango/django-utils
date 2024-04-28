from django import template
from django.template import Template, Variable, VariableDoesNotExist, TemplateSyntaxError

register = template.Library()


class RenderTemplateNode(template.Node):
    def __init__(self, content):
        self.content = Variable(content)

    def render(self, context):
        try:
            resolved_content = self.content.resolve(context)
            return Template(resolved_content).render(context)
        except (VariableDoesNotExist, TemplateSyntaxError):
            return ''


@register.tag
def render_template(parser, token):
    try:
        tag_name, value = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(f"{tag_name} tag requires at least one argument.")

    return RenderTemplateNode(value)
