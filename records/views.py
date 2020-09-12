from django.http import JsonResponse
from django.db.models import Q
from shared import *
from equipment.models import Equipment
from .models import RentalRecord


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
    records = RentalRecord.objects.filter(q)
    total = len(records)
    page = params.get('page')
    size = params.get('size')
    if page or size:
        page = int(page or 1)
        size = int(size or 10)
        records = records[(page - 1) * size: page * size]
    return JsonResponse({
        'total': total,
        'list': list(map(RentalRecord.todict, records))
    })
