from django.shortcuts import render
from blogs.models import Blog, Post
from posts.utils import wrap_plain, wrap_tags


def index(request):

    posts = Post.objects.all().order_by('-date_created')
    wrap_plain(posts)
    for post in posts:
        wrap_tags(post)  # Wrap the tags with blog info
    context = {}
    context['posts'] = posts
    return render(request, "portal/index.html", context)
