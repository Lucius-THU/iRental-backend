from django.http import JsonResponse
from .models import User
from .utils import require


@require('post', None)
def login(request):
    params = request.params
    user = User.objects.filter(email=params['email']).first()
    if user and user.authenticate(params['password']):
        request.session['user_id'] = user.id
        return JsonResponse({'user_id': user.id})
    return JsonResponse({'error': 'failed'})


@require('post', 'user')
def logout(request):
    request.session.delete()
    return JsonResponse({})
