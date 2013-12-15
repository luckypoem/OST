from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from blogs.views import blog as blog_view
from blogs.models import Blog, Post
from .forms import PostForm


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
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.blog = blog
            post.save()
            form.save_m2m()
            return HttpResponseRedirect(
                reverse('post', kwargs={'blog_slug': blog.slug,
                                        'post_slug': post.slug}))
    else:
        form = PostForm()
    context['blog'] = blog
    context['form'] = form
    return render(request, "posts/create.html", context)


def tag(request):
    pass


def post(request, blog_slug, post_slug):
    """Individual post page: /blogs/<slug>/post/<post_slug>"""
    try:
        blog = Blog.objects.get(slug=blog_slug)
    except:
        return HttpResponseRedirect(
            reverse('blog', kwargs={'slug': blog.slug}))
    try:
        post = Post.objects.get(slug=post_slug)
    except:
        return HttpResponseRedirect(
            reverse('blog', kwargs={'slug': blog.slug}))

    context = {}
    context['blog'] = blog
    context['post'] = post
    return render(request, "posts/post.html", context)

