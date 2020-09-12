from django.http import JsonResponse
from shared import *
from .models import Notification


@require('get', 'user')
def index(request):
    objs = request.user.notification_set.all()
    return JsonResponse({
        'list': list(map(modeltodict, objs))
    })


@require('post', 'user')
def update(request):
    q = {'unread': True}
    id = request.params.get('id')
    if id is not None:
        q['id'] = id
    request.user.notification_set.filter(**q).update(unread=False)
    return JsonResponse({})
