from django.urls import path
from app_core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send-email/', views.form_sendEmail, name='send-email'),
]
