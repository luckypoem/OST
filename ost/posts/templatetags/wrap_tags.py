from django import template
register = template.Library()


@register.filter('join_tag_link')
def join_tag_link(value, arg):
    from django.utils.html import conditional_escape
    arr = []
    for t in value:
        arr.append('<a href="%s">%s</a>' % (
            t.get_absolute_url(), conditional_escape(t)
        ))

    return arg.join(arr)
