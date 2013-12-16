from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from blogs.views import blog as blog_view
from blogs.models import Blog, Post
from taggit.models import Tag
from .forms import PostForm
from .utils import wrap_tags, wrap_plain
from blogs.utils import is_follower


def index(request, slug):
    """
    Redirected to blogs.view.blog
    """
    return HttpResponseRedirect(reverse('blog', kwargs={'slug': slug}))


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
            # Retain POST data and errors if invalid
            initial = {
                'title': request.POST.get('title'),
                'tags': request.POST.get('tags'),
            }
            form.initial = initial
    else:
        form = PostForm()
    context['blog'] = blog
    context['form'] = form
    return render(request, "posts/create.html", context)


def dashboard(request, slug):
    """Global portal: /blogs/<slug>/posts/dashboard/"""
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        return HttpResponseRedirect(
            reverse('blog', kwargs={'slug': blog.slug}))

    if request.user not in blog.authors.all():
        raise PermissionDenied

    context = {}
    posts = Post.objects.filter(blog=blog, author=request.user)
    posts = posts.order_by('-date_created')
    context['blog'] = blog
    context['posts'] = posts
    return render(request, "posts/dashboard.html", context)


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

    wrap_tags(post)  # Wrap the tags with blog info
    context = {}
    context['blog'] = blog
    context['post'] = post
    request.user.is_follower = is_follower(request.user, blog)
    return render(request, "posts/post.html", context)


@login_required
def edit(request, blog_slug, post_slug):
    """Individual post edit page: /blogs/<slug>/post/<post_slug>/edit/"""
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

    if request.user != post.author:
        raise PermissionDenied

    context = {}
    initial = {
        'title': post.title,
        'tags': ','.join([t.name for t in post.tags.all()]),
        'content': post.content,
    }
    if request.method == 'POST':
        if request.POST.get('submit') == 'delete':
            post.delete()
            return HttpResponseRedirect(
                reverse('blog', kwargs={'slug': blog.slug}))
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('post', kwargs={'blog_slug': blog.slug,
                                        'post_slug': post.slug}))
        else:
            # Retain POST data and errors if invalid
            initial = {
                'title': request.POST.get('title'),
                'tags': request.POST.get('tags'),
            }
            form.initial = initial
    else:
        form = PostForm(instance=post)
        form.initial = initial
    context['blog'] = blog
    context['form'] = form
    return render(request, "posts/edit.html", context)


def tag(request, blog_slug, tag_slug):
    try:
        blog = Blog.objects.get(slug=blog_slug)
    except:
        return HttpResponseRedirect(
            reverse('blog', kwargs={'slug': blog.slug}))
    context = {'blog': blog}
    try:
        tag = Tag.objects.get(slug=tag_slug)
    except:
        tag = None
    context['tag'] = tag
    if tag:
        posts = Post.objects.filter(tags=tag, blog=blog)
        posts = posts.order_by('-date_created')
        wrap_plain(posts)
        for post in posts:
            wrap_tags(post)
    else:
        posts = None
    context['posts'] = posts
    request.user.is_follower = is_follower(request.user, blog)
    return render(request, "posts/tag.html", context)
