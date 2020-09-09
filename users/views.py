from django.http import JsonResponse


def login(request):
    return JsonResponse(request.params)
