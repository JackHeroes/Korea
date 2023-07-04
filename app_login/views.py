from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

def form_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']

        # Verificar se o nome de usuário já existe
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Este nome de usuário já está em uso.'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Este email já está em uso.'})

        # Cadastrar o novo usuário
        user = User.objects.create_user(username=username, first_name=firstName, last_name=lastName, email=email, password=password)
        login(request, user)
        return redirect('home')
        
    return render(request, 'register.html')

def form_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Credenciais inválidas.'})
    else:
        return render(request, 'login.html')
