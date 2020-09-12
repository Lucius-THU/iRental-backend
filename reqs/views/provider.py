from django.http import JsonResponse
from django.db.models import Q
from shared import *
from equipment.models import Equipment
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
    params = request.params
    r = ProviderRequest.objects.create(**{
        'user': request.user,
        'info': params['info'],
    })
    return JsonResponse(modeltodict(r))


@require('get', 'user')
def query(request):
    params = request.GET
    q = {}
    for k, v in params.items():
        if k in ['id', 'user_id']:
            q[k] = v
    reqs = get_provider_reqs(request).filter(**q)
    return JsonResponse({
        'list': list(map(modeltodict, reqs))
    })


@require('post', 'admin')
def update(request, id):
    r = get_provider_reqs(request, id)
    if not r.exists():
        raise ValueError('not found')
    if request.params['approved']:
        r.update(approved=True, rejected=False)
        user = r[0].user
        user.group = 'provider'
        user.save()
    else:
        r.update(approved=False, rejected=True)
    return JsonResponse({})
