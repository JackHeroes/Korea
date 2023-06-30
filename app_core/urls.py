from django.urls import path
from app_core import views

urlpatterns = [
    path('', views.enviar_email, name='enviar_email'),
]