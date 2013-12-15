import json
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Blog


@login_required
@require_POST
def authors(request, slug):
    """Querying authors"""
    query_type = request.POST.get("type")
    data = {
        "success": False,
        "code": 1,
        "message": "This blog does not exist.",
    }
    #print slug
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        return HttpResponse(json.dumps(data), content_type="application/json")

    if request.user != blog.creator:
        data["code"] = 2
        data["message"] = "Permission denied."
        return HttpResponse(json.dumps(data), content_type="application/json")

    if query_type == "get_authors":
        authors = blog.authors.filter(~Q(username=request.user.username))
        data = [
            {
                "username": author.username,
            }
            for author in authors
        ]
        return HttpResponse(json.dumps(data), content_type="application/json")

    elif query_type == "add_author":
        author_username = request.POST.get("author")
        try:
            author = User.objects.get(username=author_username)
        except:
            data["code"] = 3
            data["message"] = "This user does not exist."
            return HttpResponse(
                json.dumps(data), content_type="application/json")

        if author in blog.authors.all():
            data["code"] = 4
            data["message"] = "This user is already an author of this blog."
            return HttpResponse(
                json.dumps(data), content_type="application/json")

        # Successful action
        blog.authors.add(author)
        data["success"] = True
        data["code"] = 0
        del data["message"]
        return HttpResponse(
            json.dumps(data), content_type="application/json")

    elif query_type == "remove_author":
        author_username = request.POST.get("author")
        try:
            author = User.objects.get(username=author_username)
        except:
            data["code"] = 3
            data["message"] = "This user does not exist."
            return HttpResponse(
                json.dumps(data), content_type="application/json")

        if author not in blog.authors.all():
            data["code"] = 5
            data["message"] = "This user is not an author of this blog."
            return HttpResponse(
                json.dumps(data), content_type="application/json")

        if author == blog.creator:
            data["code"] = 6
            data["message"] = "You cannot remove creator author."
            return HttpResponse(
                json.dumps(data), content_type="application/json")

        # Successful action
        blog.authors.remove(author)
        data["success"] = True
        data["code"] = 0
        del data["message"]
        print data
        return HttpResponse(json.dumps(data), content_type="application/json")
