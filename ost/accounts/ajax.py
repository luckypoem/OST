import json
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.http import require_GET

FETCH_LIMIT = 8


@require_GET
def users(request):
    """Query users"""
    query = request.GET.get('query')
    users = User.objects.filter(username__istartswith=query)[:FETCH_LIMIT]
    data = [
        {
            'name': user.username,
            'value': user.username,
        }
        for user in users
    ]
    return HttpResponse(json.dumps(data), content_type="application/json")
