from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Blog, Post
from .forms import BlogCreationForm
from posts.utils import wrap_plain, wrap_tags


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
        form = BlogCreationForm()
    context['form'] = form
    return render(request, "blogs/create.html", context)


@login_required
def following(request):
    return None


def blog(request, slug):
    """Individual blog view, showing all posts contained"""
    context = {}
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        blog = None
    context['blog'] = blog
    if blog:
        posts = Post.objects.filter(blog=blog).order_by('-date_created')
        wrap_plain(posts)
        for post in posts:
            wrap_tags(post)  # Wrap the tags with blog info
        context['posts'] = posts
    return render(request, "posts/index.html", context)


@login_required
def settings(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        return HttpResponseRedirect(
            reverse('blog', kwargs={'slug': blog.slug}))
    context = {}
    if request.method == 'POST':
        print request.POST
        form = BlogCreationForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('blog', kwargs={'slug': blog.slug}))
    else:
        form = BlogCreationForm(instance=blog)
    context['form'] = form
    context['blog'] = blog
    return render(request, "blogs/settings.html", context)


@login_required
def follow(request):
    pass


@login_required
def unfollow(request):
    pass
