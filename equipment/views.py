import dateutil.parser as dtparser
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.db.models import Q
from common import *
from .models import Equipment


def get_equipment(request, id):
    user = request.user
    q = Q(id=id)
    if not user.is_admin():
        q &= Q(provider=user)
    return Equipment.objects.filter(q)


@require('get', 'user')
def index(request):
    params = request.GET
    q = {}
    for key in ['name', 'id', 'user_id', 'provider_id']:
        if key in params:
            q[key] = params[key]
    q = Q(**q)
    user = request.user
    if not user.is_provider():
        q &= Q(launched=True)
    elif not user.is_admin():
        q &= Q(launched=True) | Q(provider_id=user.id)
    result = Equipment.objects.filter(q)
    total = len(result)
    page = params.get('page')
    size = params.get('size')
    if page or size:
        page = page or 1
        size = size or 10
        result = result[(page - 1) * size:page * size]
    return JsonResponse({
        'total': total,
        'list': list(map(modeltodict, result))
    })


@require('post', 'provider')
def create(request):
    data = request.params
    e = Equipment.objects.create(**{
        'name': data['name'],
        'address': data['address'],
        'expire_at': dtparser.parse(data['expire_at']),
        'provider': request.user
    })
    return JsonResponse(modeltodict(e))


@require('post', 'provider')
def update(request, id):
    data = request.POST
    equipment_set = get_equipment(request, id)
    if len(equipment_set) == 0:
        raise ValueError('The equipment does not exist')
    else:
        if 'name' in data:
            equipment_set[0].name = data['name']
        if 'address' in data:
            equipment_set[0].address = data['address']
        if 'expired_at' in data:
            equipment_set[0].expired_at = data['expired_at']
        equipment_set[0].save()
    return JsonResponse({})


@require('post', 'provider')
def delete(request, id):
    equipment_set = get_equipment(request, id)
    if len(equipment_set) == 0:
        raise ValueError('The equipment does not exist')
    else:
        equipment_set.delete()
    return JsonResponse({})


@require('post', 'provider')
def request(request, id):
    equipment_set = get_equipment(request, id)
    if len(equipment_set) == 0:
        raise ValueError('The equipment does not exist')
    else:
        equipment_set[0].requesting = True
        equipment_set[0].save()
    return JsonResponse({})


@require('post', 'provider')
def discontinue(request, id):
    equipment_set = get_equipment(request, id)
    if len(equipment_set) == 0:
        raise ValueError('The equipment does not exist')
    else:
        equipment_set[0].launched = False
        equipment_set[0].save()
    return JsonResponse({})


@require('post', 'admin')
def launch(request, id):
    equipment_set = get_equipment(request, id)
    if len(equipment_set) == 0:
        raise ValueError('The equipment does not exist')
    else:
        equipment_set[0].launched = True
        equipment_set[0].save()
    return JsonResponse({})


# This should be in requests/rental/<id>/update
# def rent(request, id, user):
#     equipment_set = get_equipment(request, id)
#     if len(equipment_set) == 0:
#         raise ValueError('The equipment does not exist')
#     else:
#         if equipment_set[0].user is not None:
#             raise ValueError('The equipment has been rented')
#         else:
#             equipment_set[0].user = user
#     return JsonResponse({})
