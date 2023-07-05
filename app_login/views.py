from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages

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

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            reset_url = f"{settings.BASE_URL}/redefinePassword/{user.id}/{token}"
            subject = 'Redefinição de Senha'
            message = f'Clique no link a seguir para redefinir sua senha: {reset_url}'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            messages.success(request, 'Um email com instruções para redefinir a senha foi enviado para o seu endereço de email.')

            if request.user.is_authenticated:
                return redirect('account')  # Redireciona para a página de conta se o usuário estiver logado
            else:
                return redirect('login')  # Redireciona para a página de login se o usuário não estiver logado
        except User.DoesNotExist:
            messages.error(request, 'O email fornecido não está associado a uma conta.')
    
    return render(request, 'forgotPassword.html')

def redefinePassword(request, user_id, reset_code):
    # Verificar se o usuário com o ID fornecido existe
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')
        return redirect('login')  # Redirecionar para a página de login ou outra adequada

    # Verificar se o código de redefinição é válido para o usuário
    if not default_token_generator.check_token(user, reset_code):
        messages.error(request, 'Código de redefinição de senha inválido.')
        return redirect('login')  # Redirecionar para a página de login ou outra adequada

    if request.method == 'POST':
        newPassword1 = request.POST.get('newPassword1')
        newPassword2 = request.POST.get('newPassword2')

        if newPassword1 != newPassword2:
            messages.error(request, 'As senhas não coincidem.')
        else:
            user.set_password(newPassword1)
            user.save()
            # Realizar o login manualmente após a redefinição da senha
            user = authenticate(request, email=user.email, password=newPassword1)
            if user is not None:
                login(request, user)

            messages.success(request, 'Senha redefinida com sucesso!')
            return redirect('account')  # Redirecionar para a página de conta após a redefinição da senha
                
    else:
        messages.error(request, 'Corrija os erros abaixo.')

    context = {
        'user_id': user_id,
        'reset_code': reset_code,
    }

    return render(request, 'redefinePassword.html', context)

@login_required
def account(request):
    return render(request, 'account.html')

@login_required
def form_logout(request):
    logout(request)
    return redirect('home')

@login_required
def form_deleteAccount(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home') 