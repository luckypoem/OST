from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Blog
from .forms import BlogCreationForm


@login_required
def index(request):
    blogs = request.user.created_blogs
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


def blog(request, slug=None):
    """Individual blog view"""
    context = {}
    if slug is None:
        return HttpResponseRedirect('/')
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        blog = None
    context['blog'] = blog
    return render(request, "blogs/blog.html", context)


def post(request, blog_slug, post_slug):
    return None
