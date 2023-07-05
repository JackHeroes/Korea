from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'index.html')
    
def form_sendEmail(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        sender = settings.EMAIL_HOST_USER
        recipient = 'JohnHeroes@outlook.com.br'
        subject = 'Novo formulário de contato recebido'
        
        text = f'''
        Nome: {name}
        E-mail: {email}
        Mensagem: {message}
        '''

        try:
            send_mail(
                subject = subject,
                message = text,
                from_email = sender,
                recipient_list = [recipient],
                fail_silently = False,
            )

            messages.success(request, 'Formulário enviado com sucesso!')
        except Exception as e:
            messages.error(request, 'Erro ao enviar formulário.')
            
    return render(request, 'index.html')
    