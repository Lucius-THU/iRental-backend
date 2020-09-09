import json
from collections import defaultdict


class ParseJsonParams:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.content_type == 'application/json':
            request.params = json.loads(request.body, **{
                'object_hook': lambda d: defaultdict(lambda: None, d)
            })
        return self.get_response(request)
