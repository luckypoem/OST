from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from blogs.models import Blog


def index(request):
    blogs = request.user.created_blogs
    context = {
        'blogs': blogs,
    }
    return render(request, "blogs/index.html", context)


def create(request):
    return None


def following(request):
    return None
