import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    if not text:
        return ""
    # Convert Markdown to HTML
    html = markdown.markdown(
        text,
        extensions=[
            'fenced_code',
            'codehilite',
            'tables',
            'toc',
            'nl2br'
        ]
    )
    return mark_safe(html)  # mark safe since markdown returns HTML
