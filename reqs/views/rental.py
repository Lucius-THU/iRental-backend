import dateutil.parser as dtparser
from django.http import JsonResponse
from django.db.models import Q
from shared import *
from reqs.models import RentalRequest


def get_rental_requests(request, id):
    user = request.user
    q = Q()
    if id is not None:
        q &= Q(id=id)
    if not user.isprovider():
        q &= Q(user=user)
    elif not user.isadmin():
        q &= Q(user=user) | Q(equipment__in=user.equipment_set.all())
    return RentalRequest.objects.filter(q)


@require('post', 'user')
def create(request):
    params = request.params
    r = RentalRequest.objects.create(**{
        'user': request.user,
        'equipment_id': params['equipment_id'],
        'purpose': params['purpose'],
        'expire_at': dtparser.parse(params['expire_at', str]),
    })
    return JsonResponse(modeltodict(r))


@require('get', 'user')
def query(request):
    params = request.GET
    q = {}
    for k, v in params.items():
        if k in ['id', 'user_id', 'equipment_id']:
            q[k] = v
    result = get_rental_requests(request, None).filter(**q)
    total = len(result)
    page = params.get('page')
    size = params.get('size')
    if page or size:
        page = int(page or 1)
        size = int(size or 10)
        result = result[(page - 1) * size: page * size]
    return JsonResponse({
        'total': total,
        'list': list(map(modeltodict, result))
    })


@require('post', 'provider')
def update(request, id):
    r = get_rental_requests(request, id)
    if not r.exists():
        raise ValueError('not found')
    if request.params['approved']:
        r.update(approved=True, rejected=False)
    else:
        r.update(approved=False, rejected=True)
    return JsonResponse({})


@require('post', 'admin')
def delete(request, id):
    r = get_rental_requests(request, id)
    if not r.exists():
        raise ValueError('not found')
    r.delete()
    return JsonResponse({})
