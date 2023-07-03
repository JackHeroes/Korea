from django.urls import path
from app_core import views

urlpatterns = [
    path('', views.sendEmail, name='sendEmail'),
]