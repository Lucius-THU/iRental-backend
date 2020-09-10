from django.http import HttpResponse, JsonResponse
from common import *
from .models import User


@require('post', None)
def signup(request):
    params = request.params
    user = User.create(**{
        'email': params['email'],
        'password': params['password']
    })
    return JsonResponse({'id': user.id})


@require('post', None)
def login(request):
    params = request.params
    user = User.objects.filter(email=params['email']).first()
    if user and user.authenticate(params['password']):
        request.session['user_id'] = user.id
        return JsonResponse(modeltodict(user, exclude='password'))
    return HttpResponse(status=400)


@require('post', 'user')
def logout(request):
    request.session.delete()
    return JsonResponse({})


@require('get', 'user')
def current(request):
    user = request.user
    return JsonResponse(modeltodict(user, exclude='password'))
