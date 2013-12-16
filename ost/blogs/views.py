from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Blog, Post
from .forms import BlogCreationForm
from posts.utils import wrap_plain, wrap_tags
from .utils import is_follower


@login_required
def index(request):
    created_blogs = list(request.user.created_blogs.order_by('-date_created'))
    authored_blogs = [
        blog for blog in request.user.authored_blogs.order_by('-date_created')
        if blog not in created_blogs
    ]
    blogs = created_blogs + authored_blogs
    context = {
        'blogs': blogs,
    }
    return render(request, "blogs/index.html", context)


@login_required
def create(request):
    context = {}
    if request.method == 'POST':
        form = BlogCreationForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.creator = request.user
            blog.save()
            blog.authors.add(request.user)
            form.save_m2m()
            return HttpResponseRedirect(
                reverse('blog', kwargs={'slug': blog.slug}))
        else:
            # Retain POST data if invalid
            data = {
                'name': request.POST.get('name'),
            }
            form.initial = data
            context['form'] = form
    else:
        form = BlogCreationForm()
    context['form'] = form
    return render(request, "blogs/create.html", context)


@login_required
def following(request):
    blogs = Blog.objects.filter(followers=request.user)
    posts = Post.objects.filter(blog__in=blogs).order_by('-date_created')
    wrap_plain(posts)
    for post in posts:
        wrap_tags(post)
    context = {
        'posts': posts
    }
    return render(request, "blogs/following.html", context)


def blog(request, slug):
    """Individual blog view, showing all posts contained"""
    context = {}
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        raise Http404
    context['blog'] = blog
    if blog:
        posts = Post.objects.filter(blog=blog).order_by('-date_created')
        wrap_plain(posts)
        for post in posts:
            wrap_tags(post)  # Wrap the tags with blog info
        context['posts'] = posts
    num_posts = Post.objects.filter(blog=blog).count()
    context['num_posts'] = num_posts
    if request.user.is_authenticated() and blog:
        request.user.is_follower = is_follower(request.user, blog)
    return render(request, "posts/index.html", context)


@login_required
def settings(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        return HttpResponseRedirect(
            reverse('blog', kwargs={'slug': slug}))
    context = {}

    if request.user != blog.creator:
        raise PermissionDenied

    if request.method == 'POST':
        if request.POST.get('submit') == 'delete':
            blog.delete()
            return HttpResponseRedirect(reverse('blogs:index'))
        form = BlogCreationForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('blog', kwargs={'slug': blog.slug}))
        else:
            # Retain POST data if invalid
            data = {
                'name': request.POST.get('name'),
            }
            form = BlogCreationForm(initial=data)
            context['form'] = form
    else:
        form = BlogCreationForm(instance=blog)
    context['form'] = form
    context['blog'] = blog
    return render(request, "blogs/settings.html", context)


def search(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        return HttpResponseRedirect(
            reverse('blog', kwargs={'slug': blog.slug}))
    query = request.GET.get('query')
    posts = Post.objects.filter(blog=blog, content__search=query)
    wrap_plain(posts)
    context = {'posts': posts, 'blog': blog, 'query': query}
    return render(request, "posts/search.html", context)
