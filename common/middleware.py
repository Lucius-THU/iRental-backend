import json
# from collections import defaultdict
from django.http import HttpResponse, JsonResponse


class paramsdict(dict):
    def __getitem__(self, key):
        cls = None
        if isinstance(key, tuple):
            key, cls = key
        value = super().__getitem__(key)
        if cls is not None:
            if not isinstance(value, cls):
                s = 'field "%s" has to be of type "%s"'
                raise TypeError(s % (key, cls.__name__))
        return value

    def get(self, key):
        if key not in self:
            return None
        return super().__getitem__(key)


class JsonMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.content_type == 'application/json':
            # request.params = json.loads(request.body)
            request.params = json.loads(request.body, **{
                # 'object_hook': lambda d: defaultdict(lambda: None, d)
                'object_hook': paramsdict
            })
        # elif request.method == 'POST':
        #     return HttpResponse(status=400)
        return self.get_response(request)


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        s = str(exception)
        if isinstance(exception, KeyError):
            return JsonResponse({'error': f'field "{s[1:-1]}" is required'})
        return JsonResponse({'error': s})
