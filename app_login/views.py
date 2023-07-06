from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail, EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib import messages
import re

User = get_user_model()

# Create your views here.

def form_register(request):
    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está em uso.')
            return render(request, 'register.html')

        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            messages.error(request, 'A senha deve conter letras, números, pelo menos um caractere especial e ter no mínimo 8 caracteres.')
            return render(request, 'register.html')

        user = User.objects.create_user(email=email, first_name=firstName, last_name=lastName, password=password)
        user.is_active = False
        user.save()
        activateEmail(request, user)
        return redirect('home')
        
    return render(request, 'register.html')

def activateEmail(request, user):
    mail_subject = 'Ative sua conta de usuário.'
    message = render_to_string('activateAccount.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    email = EmailMessage(mail_subject, message, to=[user.email])
    if email.send():
        messages.success(request, f'Prezado(a) {user.first_name}, por favor, vá para a caixa de entrada do seu e-mail {user.email} e clique no link de ativação recebido para confirmar e completar o registro. Observação: Verifique sua pasta de spam.')
    else:
        messages.error(request, f'Problema ao enviar o e-mail de confirmação para {user.email}, verifique se você digitou corretamente o endereço de e-mail.')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Obrigado pela confirmação do seu email. Agora você pode fazer login na sua conta.')
        return redirect('login')
    else:
        messages.error(request, 'O link de ativação é inválido!')

    return redirect('home')

def form_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                messages.error(request, 'Senha incorreta.')
                return render(request, 'login.html')
            if not user.is_active:
                messages.error(request, 'Sua conta ainda não foi verificada.')
                return render(request, 'login.html')
            login(request, user)
            return redirect('home')
        except User.DoesNotExist:
            messages.error(request, 'E-mail não encontrado.')
        
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if request.user.is_authenticated and request.user.email != email:
            messages.error(request, 'Email incorreto.')
            return render(request, 'forgotPassword.html')
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
