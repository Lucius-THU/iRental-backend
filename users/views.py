from django.http import HttpResponse, JsonResponse
from common import require
from .models import User


@require('post', None)
def login(request):
    params = request.params
    user = User.objects.filter(email=params['email']).first()
    if user and user.authenticate(params['password']):
        request.session['user_id'] = user.id
        return JsonResponse({'user_id': user.id})
    return HttpResponse(status=400)


@require('post', 'user')
def logout(request):
    request.session.delete()
    return JsonResponse({})
