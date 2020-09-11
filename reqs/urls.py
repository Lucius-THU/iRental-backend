from django.urls import include, path
from .views import rental
from .views import provider

urlpatterns = [
    path('rental/', include([
        path('create', rental.create),
        path('', rental.query),
        path('<int:id>/update', rental.update),
        path('<int:id>/delete', rental.delete),
    ])),
    path('provider/', include([
        path('create', provider.create),#提供者申请的创建
        path('', provider.query),#查询
        path('<int:id>/update', provider.update),#审核
    ])),
]
