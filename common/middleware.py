import json
from collections import defaultdict
from django.http import HttpResponse, JsonResponse


class JsonMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.content_type == 'application/json':
            request.params = json.loads(request.body, **{
                'object_hook': lambda d: defaultdict(lambda: None, d)
            })
        elif request.method == 'POST':
            return HttpResponse(status=400)
        return self.get_response(request)


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        return JsonResponse({'error': str(exception)})
