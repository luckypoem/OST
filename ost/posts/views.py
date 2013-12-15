from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from blogs.views import blog as blog_view
from blog.models import Blog


def index(request, slug):
    """
    Alias of blogs.view.blog
    Global portal: /blogs/<blog_slug>/posts/
    """
    return blog_view(request, slug)


@login_required
def create(request, slug):
    """Global portal: /blogs/<slug>/posts/create/"""
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        return HttpResponseRedirect(
            reverse('blog', kwargs={'slug': blog.slug}))

    if request.user not in blog.authors.all():
        raise PermissionDenied

    context = {}
    return render(request, "posts/create.html", context)


def tag(request):
    pass


def post(request):
    """Individual post page: /blogs/<slug>/post/<post_slug>"""
    pass
