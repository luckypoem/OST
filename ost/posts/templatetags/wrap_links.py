from django import template
register = template.Library()
from django.core.urlresolvers import reverse


@register.filter('join_tag_link')
def join_tag_link(value, arg):
    from django.utils.html import conditional_escape
    arr = []
    for t in value:
        arr.append('<a href="%s">%s</a>' % (
            reverse('tag', args=(t['blog_slug'], t['tag_slug'])), t['name']
        ))
    return arg.join(arr)


@register.filter('join_name_link')
def join_name_link(value, arg):
    from django.utils.html import conditional_escape
    arr = []
    for t in value:
        arr.append('<a href="%s">%s</a>' % (
            t.get_absolute_url(), t.name,
        ))
    return arg.join(arr)
