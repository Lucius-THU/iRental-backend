from django.http import JsonResponse
from django.db.models import Count
from shared import *
from users.models import User
from equipment.models import Equipment


@require('get', 'admin')
def top_users(request):
    n = int(request.GET.get('count') or 3)
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
