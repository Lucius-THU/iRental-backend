from django.http import JsonResponse
from django.db.models import Count
from shared import *
from users.models import User
from equipment.models import Equipment


@require('get', 'admin')
def top_users(request):
    params = request.GET
    n = int(params.get('count') or 3)
    key = params.get('key')
    if key == 'request':
        users = User.objects \
            .annotate(request_count=Count('rentalrequest')) \
            .order_by('-request_count', '-id')[:n]
    else:
        users = User.objects \
            .annotate(rental_count=Count('rentalrecord')) \
            .order_by('-rental_count', '-id')[:n]
    return JsonResponse({
        'list': list(map(User.todict, users))
    })


@require('get', 'admin')
def top_equipment(request):
    n = int(request.GET.get('count') or 3)
    equipment = Equipment.objects \
        .annotate(rental_count=Count('rentalrecord')) \
        .order_by('-rental_count', '-id')[:n]
    return JsonResponse({
        'list': list(map(Equipment.todict, equipment))
    })
