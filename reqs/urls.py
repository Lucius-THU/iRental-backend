from django.urls import include, path
from .views import rental

urlpatterns = [
    path('rental/', include([
        path('create', rental.create),
        path('', rental.query),
        path('<int:id>/update', rental.update),
        path('<int:id>/delete', rental.delete),
    ])),
]
