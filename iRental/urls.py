from django.urls import include, path

apipatterns = [
    path('', include('users.urls.auth')),
    path('equipment/', include('equipment.urls')),
    # path('requests/', include('reqs.urls')),
    # path('records/', include('records.urls')),
]

urlpatterns = [
    path('api/', include(apipatterns))
]
