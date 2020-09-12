import dateutil.parser as dtparser
from django.http import JsonResponse
from django.db.models import Q
from shared import *
from equipment.models import Equipment
from records.models import RentalRecord
from ..models import RentalRequest


@require('post', 'user')
def create(request):
    params = request.params
    e = Equipment.objects.filter(id=params['equipment_id']).first()
    if e is None or not e.launched:
        raise ValueError('not avaliable')
    try:
        rent_until = dtparser.parse(params['expire_at'])
    except BaseException:
        rent_until = dtparser.parse(params['rent_until', str])
    r = RentalRequest.objects.create(**{
        'user': request.user,
        'equipment': e,
        'purpose': params['purpose'],
        'rent_until': rent_until,
    })
    return JsonResponse(r.todict())


@require('get', 'user')
def query(request):
    params = request.GET
    user = request.user
    q = Q()
    if not user.isprovider():
        q &= Q(user=user)
    if params.get('provided') == '1':
        e = Equipment.objects.filter(provider_id=user.id)
        q &= Q(equipment__in=e)
    elif not user.isadmin():
        q &= Q(user=user)
    for k, v in params.items():
        if k in ['id', 'user_id', 'equipment_id']:
            q &= Q(**{k: v})
    reqs = RentalRequest.objects.filter(q)
    total = len(reqs)
    page = params.get('page')
    size = params.get('size')
    if page or size:
        page = int(page or 1)
        size = int(size or 10)
        reqs = reqs[(page - 1) * size: page * size]
    return JsonResponse({
        'total': total,
        'list': list(map(RentalRequest.todict, reqs))
    })


@require('post', 'provider')
def update(request, id):
    user = request.user
    q = Q(id=id)
    if not user.isadmin():
        q &= Q(equipment__in=user.equipment_set.all())
    r = RentalRequest.objects.filter(q)
    if not r.exists():
        raise ValueError('not found')
    if request.params['approved']:
        r.update(approved=True, rejected=False)
        e = r[0].equipment
        e.user = r[0].user
        e.rent_until = r[0].rent_until
        e.save()
        RentalRecord.objects.create(**{
            'user': e.user,
            'equipment': e,
            'returned': False
        })
    else:
        r.update(approved=False, rejected=True)
    return JsonResponse({})


@require('post', 'admin')
def delete(request, id):
    r = RentalRequest.objects.filter(id=id)
    if not r.exists():
        raise ValueError('not found')
    r.delete()
    return JsonResponse({})
