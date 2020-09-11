import dateutil.parser as dtparser
from django.http import JsonResponse
from django.db.models import Q
from shared import *
from equipment.models import Equipment
from reqs.models import RentalRequest


def get_rental_reqs(request, id = None, only_editable = False):
    user = request.user
    q = Q(id=None)
    if user.isadmin():
        q |= ~Q(id=None)
    elif user.isprovider():
        q |= Q(equipment__in=user.equipment_set.all())
    if not only_editable:
        q |= Q(user=user)
    if id is not None:
        q &= Q(id=id)
    return RentalRequest.objects.filter(q)


@require('post', 'user')
def create(request):
    params = request.params
    e = Equipment.objects.filter(id=params['equipment_id']).first()
    if e is None or not e.launched:
        raise ValueError('not avaliable')
    r = RentalRequest.objects.create(**{
        'user': request.user,
        'equipment': e,
        'purpose': params['purpose'],
        'rent_until': dtparser.parse(params['rent_until', str]),
    })
    return JsonResponse(modeltodict(r))


@require('get', 'user')
def query(request):
    params = request.GET
    q = {}
    for k, v in params.items():
        if k in ['id', 'user_id', 'equipment_id']:
            q[k] = v
    reqs = get_rental_reqs(request).filter(**q)
    total = len(reqs)
    page = params.get('page')
    size = params.get('size')
    if page or size:
        page = int(page or 1)
        size = int(size or 10)
        reqs = reqs[(page - 1) * size: page * size]
    return JsonResponse({
        'total': total,
        'list': list(map(modeltodict, reqs))
    })


@require('post', 'provider')
def update(request, id):
    r = get_rental_reqs(request, id, only_editable=True)
    if not r.exists():
        raise ValueError('not found')
    if request.params['approved']:
        r.update(approved=True, rejected=False)
        e = r[0].equipment
        e.user = r[0].user
        e.rent_until = r[0].rent_until
        e.save()
    else:
        r.update(approved=False, rejected=True)
    return JsonResponse({})


@require('post', 'admin')
def delete(request, id):
    r = get_rental_reqs(request, id)
    if not r.exists():
        raise ValueError('not found')
    r.delete()
    return JsonResponse({})
