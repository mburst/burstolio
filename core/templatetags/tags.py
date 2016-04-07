from core.models import Comment, Tag

from django import template

register = template.Library()

#May want to ditch this for a middleware that passes in the comments object so that I can do the manipulations in the actual template
@register.simple_tag
def recent_comments():
    
    comments = Comment.objects.select_related('entry').filter(deleted=False, spam=False).order_by('-id')[:3]
    output = '<ul id="recent">'
    for comment in comments:
        if not comment.name:
            comment.name = "Anonymous"
        elif comment.user:
            output += '<li><a href="http://www.github.com/mburst">' + comment.user.get_full_name() + '</a> - <a href="' + comment.entry.get_absolute_url() + '">' + comment.entry.title + '</a></li>'
        else:
            output += '<li>' + comment.name + ' - <a href="' + comment.entry.get_absolute_url() + '">' + comment.entry.title + '</a></li>'
    output += '</ul>'
    return output
    
@register.simple_tag
def tags():
    tags = Tag.objects.order_by('?')[:10]
    return tags