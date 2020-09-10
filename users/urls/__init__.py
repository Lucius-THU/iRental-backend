from django.urls import path
from .. import views

urlpatterns = [
    path('', views.index),
    path('current', views.current),
    path('<int:id>', views.detail),
    path('<int:id>/update', views.update),
    path('<int:id>/delete', views.delete),
]
