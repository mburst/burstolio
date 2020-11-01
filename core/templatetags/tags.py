from core.models import Tag

from django import template

register = template.Library()
    
@register.simple_tag
def tags():
    tags = Tag.objects.order_by('?')[:10]
    return tags