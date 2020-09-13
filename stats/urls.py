from django.urls import path
from . import views

urlpatterns = [
    path('top_users', views.top_users),
    path('top_equipment', views.top_equipment),
]
