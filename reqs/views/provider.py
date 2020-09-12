from django.http import JsonResponse
from django.db.models import Q
from shared import *
from equipment.models import Equipment
from notifications.models import Notification
from ..models import ProviderRequest


def get_provider_reqs(request, id=None):
    user = request.user
    q = Q(user=user)
    if user.isadmin():
        q |= ~Q(id=None)
    if id is not None:
        q &= Q(id=id)
    return ProviderRequest.objects.filter(q)


@require('post', 'user')
def create(request):
    user = request.user
    if user.isprovider():
        raise ValueError('nothing to request')
    if ProviderRequest.objects.filter(user=user).exists():
        raise ValueError('already requested')
    r = ProviderRequest.objects.create(**{
        'user': user,
        'info': request.params['info']
    })
    return JsonResponse(r.todict())


@require('get', 'user')
def query(request):
    params = request.GET
    q = {}
    for k, v in params.items():
        if k in ['id', 'user_id']:
            q[k] = v
    reqs = get_provider_reqs(request).filter(**q)
    return JsonResponse({
        'list': list(map(ProviderRequest.todict, reqs))
    })


@require('post', 'admin')
def update(request, id):
    params = request.params
    r = get_provider_reqs(request, id)
    if not r.exists():
        raise ValueError('not found')
    if params['approved']:
        r.update(approved=True, rejected=False)
        user = r[0].user
        user.group = 'provider'
        user.save()
    else:
        r.update(approved=False, rejected=True)
    Notification.create(
        r[0].user,
        params.get('notification')
    )
    return JsonResponse({})
