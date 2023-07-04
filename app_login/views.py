from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

def form_register(request):
    return render(request, 'register.html')

def form_login(request):
    return render(request, 'login.html')
