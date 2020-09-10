import functools
from django.http import HttpResponse, JsonResponse
from users.models import User


def require(method, group = 'user'):
    method = method.upper()
    def deco(func):
        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            if request.method.upper() != method:
                return HttpResponse(status=400)
            if group is not None:
                user = User.load(request.session)
                if user is None:
                    return HttpResponse(status=403)
                if not user.in_group(group):
                    return JsonResponse({
                        'error': 'access denied'
                    })
                request.user = user
            return func(request, *args, **kwargs)
        return inner
    return deco


def modeltodict(obj, **kwargs):
    def filtered(item):
        k, v = item
        if k == '_state':
            return False
        if 'only' in kwargs:
            return k in kwargs['only']
        if 'exclude' in kwargs:
            return k not in kwargs['exclude']
        return True
    return dict(filter(filtered, vars(obj).items()))
