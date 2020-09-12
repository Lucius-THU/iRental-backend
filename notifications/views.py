from django.http import JsonResponse
from shared import *
from .models import Notification


@require('get', 'user')
def index(request):
    objs = Notification.objects.filter(user=request.user)
    return JsonResponse({
        'list': list(map(modeltodict, objs))
    })


@require('post', 'user')
def update(request):
    q = {'user': request.user}
    id = request.params.get('id')
    if id is not None:
        q['id'] = id
    Notification.objects.filter(**q).update(unread=False)
    return JsonResponse({})
