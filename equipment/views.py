from datetime import datetime, timezone
import dateutil.parser as dtparser
from django.http import JsonResponse
from django.db.models import Q
from shared import *
from notifications.models import Notification
from .models import Equipment


def get_equipment(request, id):
    user = request.user
    q = Q(id=id)
    if not user.isprovider():
        q &= Q(id=None)
    elif not user.isadmin():
        q &= Q(provider=user)
    return Equipment.objects.filter(q).first()


@require('post', 'provider')
def create(request):
    params = request.params
    e = Equipment.objects.create(**{
        'name': params['name'],
        'address': params['address'],
        'expire_at': dtparser.parse(params['expire_at', str]),
        'provider': request.user
    })
    return JsonResponse(e.todict())


@require('get', 'user')
def query(request):
    params = request.GET
    user = request.user
    q = Q()
    for k, v in params.items():
        if k not in [ f.attname for f in Equipment._meta.fields ]:
            continue
        if k != 'name':
            q &= Q(**{k: v})
        else:
            q &= Q(name__contains=v)
    if not user.isprovider():
        q &= Q(launched=True)
    elif not user.isadmin():
        q &= Q(launched=True) | Q(provider_id=user.id)
    result = Equipment.objects.filter(q)
    total = result.count()
    page = params.get('page')
    size = params.get('size')
    if page or size:
        page = int(page or 1)
        size = int(size or 10)
        result = result[(page - 1) * size: page * size]
    return JsonResponse({
        'total': total,
        'list': list(map(Equipment.todict, result))
    })


@require('post', 'provider')
def update(request, id):
    e = get_equipment(request, id)
    if e is None:
        raise ValueError('not found')
    for k, v in request.params.items():
        if k in ['name', 'address']:
            setattr(e, k, v)
        elif k == 'expire_at':
            e.expire_at = dtparser.parse(v)
    e.save()
    return JsonResponse({})


@require('post', 'provider')
def delete(request, id):
    e = get_equipment(request, id)
    if e is None:
        raise ValueError('not found')
    e.delete()
    return JsonResponse({})


@require('post', 'provider')
def request(request, id):
    e = get_equipment(request, id)
    if e is None:
        raise ValueError('not found')
    e.requesting = True
    e.save()
    return JsonResponse({})


@require('post', 'provider')
def discontinue(request, id):
    e = get_equipment(request, id)
    if e is None:
        raise ValueError('not found')
    e.launched = False
    e.requesting = False
    e.user = None
    e.rent_until = None
    e.save()
    e.rentalrecord_set.update(returned=True)
    if request.user != e.provider:
        Notification.create(
            e.provider,
            request.params.get('notification')
        )
    return JsonResponse({})


@require('post', 'admin')
def launch(request, id):
    e = get_equipment(request, id)
    if e is None:
        raise ValueError('not found')
    e.launched = True
    e.requesting = False
    e.save()
    Notification.create(
        e.provider,
        request.params.get('notification')
    )
    return JsonResponse({})


@require('post', 'user')
def close(request, id):
    user = request.user
    e = Equipment.objects.filter(user=user, id=id).first()
    if e is None:
        raise ValueError('not found')
    e.returning = True
    e.save()
    return JsonResponse({})


@require('post', 'provider')
def terminate(request, id):
    e = get_equipment(request, id)
    if e is None:
        raise ValueError('not found')
    e.user = None
    e.rent_until = None
    e.returning = False
    e.save()
    e.rentalrecord_set.filter(returned=False).update(**{
        'returned': True,
        'returned_at': utcnow()
    })
    return JsonResponse({})
