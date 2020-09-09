import json


class ParseJsonParams:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.content_type == 'application/json':
            request.params = json.loads(request.body)
        return self.get_response(request)
