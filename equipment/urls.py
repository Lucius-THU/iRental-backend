from django.urls import path
from . import views

urlpatterns = [
    path('', views.query),
    path('create', views.create),
    path('<int:id>/update', views.update),
    path('<int:id>/delete', views.delete),
    path('<int:id>/request', views.request),
    path('<int:id>/discontinue', views.discontinue),
    path('<int:id>/launch', views.launch),
]
