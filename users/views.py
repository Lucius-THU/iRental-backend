from datetime import datetime, timezone, timedelta
import secrets
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from shared import *
from .models import User, SignupRequest


def send_verification_code(email):
    if User.objects.filter(email=email).exists():
        raise ValueError('email exists')
    code = '%06d' % secrets.randbelow(10 ** 6)
    send_mail('verification code', code, None, [email])
    SignupRequest.objects.create(**{
        'email': email,
        'token': code,
        'expire_at': utcnow(minutes=10)
    })


@require('post', None)
def signup(request):
    params = request.params
    email = params['email']
    if settings.DEBUG and params.get('force'):
        password = params['password']
    else:
        token = params.get('token')
        if token is None:
            send_verification_code(email)
            return JsonResponse({})
        password = params['password']
        reqs = SignupRequest.objects.filter(**{
            'email': email,
            'token': token,
            'expire_at__gt': datetime.now(timezone.utc)
        })
        if not reqs.exists():
            raise ValueError('invalid token')
        reqs.delete()
    user = User.create(email, password)
    return JsonResponse({'id': user.id})


@require('post', None)
def login(request):
    params = request.params
    user = User.objects.filter(email=params['email']).first()
    if user and user.authenticate(params['password']):
        request.session['user_id'] = user.id
        return JsonResponse(user.todict())
    return HttpResponse(status=400)


@require('post', 'user')
def logout(request):
    request.session.delete()
    return JsonResponse({})


@require('get', 'admin')
def index(request):
    params = request.GET
    page = params.get('page')
    size = params.get('size')
    users = User.objects.all()
    total = users.count()
    if page or size:
        page = int(page or 1)
        size = int(size or 10)
        users = users[(page - 1) * size: page * size]
    return JsonResponse({
        'total': total,
        'list': list(map(User.todict, users))
    })


@require('get', 'user')
def current(request):
    user = request.user
    return JsonResponse(user.todict(True))


@require('get', 'user')
def detail(request, id):
    user = User.objects.get(id=id)
    return JsonResponse(user.todict())


@require('post', 'user')
def update(request, id):
    user = User.objects.get(id=id)
    for k, v in request.params.items():
        if k in ['name', 'address', 'contact']:
            setattr(user, k, v)
        elif k == 'group':
            if request.user.isadmin() and not user.isadmin():
                if v in ['user', 'provider']:
                    user.group = v
    user.save()
    return JsonResponse({})


@require('post', 'admin')
def delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return JsonResponse({})
