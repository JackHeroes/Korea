from django.urls import path
from app_login import views

urlpatterns = [
    path('login/', views.form_login, name='login'),
    path('register/', views.form_register, name='register'),
]
