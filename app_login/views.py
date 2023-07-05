from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import re

User = get_user_model()

# Create your views here.

def form_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está em uso.')
            return render(request, 'register.html')

        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            messages.error(request, 'A senha deve conter letras, números, pelo menos um caractere especial e ter no mínimo 8 caracteres.')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, first_name=firstName, last_name=lastName, email=email, password=password)
        login(request, user)
        messages.success(request, 'Conta criada com sucesso!')
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
            messages.error(request, 'Credenciais inválidas.')
            return render(request, 'login.html')
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
                return redirect('account')  
            else:
                return redirect('login') 
        except User.DoesNotExist:
            messages.error(request, 'O email fornecido não está associado a uma conta.')

    return render(request, 'forgotPassword.html')
    
def redefinePassword(request, user_id, reset_code):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')
    if not default_token_generator.check_token(user, reset_code):
        messages.error(request, 'Código de redefinição de senha inválido.')
    if request.method == 'POST':
        newPassword1 = request.POST.get('newPassword1')
        newPassword2 = request.POST.get('newPassword2')
        if newPassword1 != newPassword2:
            messages.error(request, 'As senhas não coincidem.')
        else:
            if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', newPassword1):
                messages.error(request, 'A senha deve conter letras, números, pelo menos um caractere especial e ter no mínimo 8 caracteres.') 
            else:
                user.set_password(newPassword1)
                user.save()
                user = authenticate(request, email=user.email, password=newPassword1)
                if user is not None:
                    login(request, user)

                messages.success(request, 'Senha redefinida com sucesso!')
                return redirect('account') 
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
        confirmation = request.POST.get('confirmation', '').strip().lower()

        if confirmation == 'excluir':
            request.user.delete()
            messages.success(request, 'Sua conta foi excluída com sucesso.')
            return redirect('home')
        else:
            messages.error(request, 'Digite "excluir" na caixa de confirmação para excluir sua conta.')
    
    return render(request, 'account.html')
