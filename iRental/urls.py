from django.urls import include, path

urlpatterns = [
    path('', include('users.urls.auth')),
    path('api/equipment', include('equipment.urls')),
    # path('api/requests', include('reqs.urls')),
    # path('api/records', include('records.urls')),
]
