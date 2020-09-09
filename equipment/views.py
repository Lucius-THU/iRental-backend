import dateutil.parser as dtparser
from django.http import HttpResponse, HttpRequest, JsonResponse
from common import *
from .models import Equipment


@require('post', 'provider')
def equipment_create(request):
    data = request.params
    Equipment.objects.create(**{
        'name': data['name'],
        'address': data['address'],
        'expire_at': dtparser.parse(data['expire_at']),
        'provider': request.user
    })
    return JsonResponse({})


@require('post', 'provider')
def equipment_request(request, id):
    existed_equipment = Equipment.objects.filter(id=id)
    if len(existed_equipment) == 0:
        raise ValueError('The equipment does not exist')
    else:
        existed_equipment[0].requesting = True
        existed_equipment[0].save()
    return JsonResponse({})


def equipment_launch(request, id):
    existed_equipment = Equipment.objects.filter(id=id)
    if len(existed_equipment) == 0:
        raise ValueError('The equipment does not exist')
    else:
        existed_equipment[0].launched = True
        existed_equipment[0].save()
    return JsonResponse({})


def equipment_rent(request, id, user):
    existed_equipment = Equipment.objects.filter(id=id)
    if len(existed_equipment) == 0:
        raise ValueError('The equipment does not exist')
    else:
        if existed_equipment[0].user is not None:
            raise ValueError('The equipment has been rented')
        else:
            existed_equipment[0].user = user
    return JsonResponse({})


def equipment_del(request, id):
    existed_equipment = Equipment.objects.filter(id=id)
    if len(existed_equipment) == 0:
        raise ValueError('The equipment does not exist')
    else:
        existed_equipment.delete()
    return JsonResponse({})


def equipment_update(request, id):
    data = request.POST
    existed_equipment = Equipment.objects.filter(id=id)
    if len(existed_equipment) == 0:
        raise ValueError('The equipment does not exist')
    else:
        if 'name' in data:
            existed_equipment[0]['name'] = data['name']
        if 'address' in data:
            existed_equipment[0]['address'] = data['address']
        if 'expired_at' in data:
            existed_equipment[0]['expired_at'] = data['expired_at']
    return JsonResponse({})


def equipment_query(request):
    data = request.GET
    total = 0
    lists = []
    if 'name' not in data and 'id' not in data:
        total = len(Equipment.objects.get())
        lists = Equipment.objects.get()
    elif 'id' in data:
        existed_equipment = Equipment.objects.filter(id=data['id'])
        if len(existed_equipment) == 0:
            raise ValueError('The equipment does not exist')
        else:
            total = 1
            lists = existed_equipment
    else:
        existed_equipment = Equipment.objects.get()
        for item in existed_equipment:
            if data['name'] in item.name:
                list.append(item)
        total = len(lists)
    response = {
        'total': total,
        'lists': lists
    }
    return JsonResponse(response)
