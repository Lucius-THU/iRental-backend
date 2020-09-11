# high-level utils

import functools
from django.http import HttpResponse, JsonResponse
from common import *
from users.models import User


def require(method, group='user'):
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
                if not user.ingroup(group):
                    return JsonResponse({
                        'error': 'access denied'
                    })
                request.user = user
            return func(request, *args, **kwargs)
        return inner
    return deco
