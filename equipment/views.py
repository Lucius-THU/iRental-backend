import dateutil.parser as dtparser
from django.http import JsonResponse
from django.db.models import Q
from shared import *
from .models import Equipment


def get_equipment_set(request, id):
    user = request.user
    q = Q(id=id)
    if not user.isadmin():
        q &= Q(provider=user)
    return Equipment.objects.filter(q)


@require('post', 'provider')
def create(request):
    params = request.params
    e = Equipment.objects.create(**{
        'name': params['name'],
        'address': params['address'],
        'expire_at': dtparser.parse(params['expire_at', str]),
        'provider': request.user
    })
    return JsonResponse(modeltodict(e))


@require('get', 'user')
def query(request):
    params = request.GET
    user = request.user
    q = Q()
    for k, v in params.items():
        if k in ['id', 'user_id', 'provider_id']:
            q &= Q(**{k: v})
        elif k == 'name':
            q &= Q(name__contains=v)
    if not user.isprovider():
        q &= Q(launched=True)
    elif not user.isadmin():
        q &= Q(launched=True) | Q(provider_id=user.id)
    result = Equipment.objects.filter(q)
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
    e = get_equipment_set(request, id).first()
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
    equipment_set = get_equipment_set(request, id)
    if len(equipment_set) == 0:
        raise ValueError('The equipment does not exist')
    else:
        equipment_set.delete()
    return JsonResponse({})


@require('post', 'provider')
def request(request, id):
    equipment_set = get_equipment_set(request, id)
    if len(equipment_set) == 0:
        raise ValueError('The equipment does not exist')
    else:
        equipment_set[0].requesting = True
        equipment_set[0].save()
    return JsonResponse({})


@require('post', 'provider')
def discontinue(request, id):
    equipment_set = get_equipment_set(request, id)
    if len(equipment_set) == 0:
        raise ValueError('The equipment does not exist')
    else:
        equipment_set[0].launched = False
        equipment_set[0].save()
    return JsonResponse({})


@require('post', 'admin')
def launch(request, id):
    equipment_set = get_equipment_set(request, id)
    if len(equipment_set) == 0:
        raise ValueError('The equipment does not exist')
    else:
        equipment_set[0].launched = True
        equipment_set[0].save()
    return JsonResponse({})


# This should be in requests/rental/<id>/update
# def rent(request, id, user):
#     equipment_set = get_equipment_set(request, id)
#     if len(equipment_set) == 0:
#         raise ValueError('The equipment does not exist')
#     else:
#         if equipment_set[0].user is not None:
#             raise ValueError('The equipment has been rented')
#         else:
#             equipment_set[0].user = user
#     return JsonResponse({})
