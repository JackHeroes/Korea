from django.urls import path
from app_core import views

urlpatterns = [
    path('', views.index, name='index'),
]