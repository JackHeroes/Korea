from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

# Create your views here.

def home(request):
    return render(request, 'index.html')
    
def form_sendEmail(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # Configuração do e-mail
        sender = settings.EMAIL_HOST_USER
        recipient = 'JohnHeroes@outlook.com.br'
        subject = 'Novo formulário de contato recebido'
        
        # Corpo do e-mail
        text = f'''
        Nome: {name}
        E-mail: {email}
        Mensagem: {message}
        '''

        try:
            # Configuração e envio do e-mail
            send_mail(
                subject = subject,
                message = text,
                from_email = sender,
                recipient_list = [recipient],
                fail_silently = False,
            )

            # Retorna uma resposta JSON indicando sucesso
            return JsonResponse({'status': 'success'})
        except Exception as e:
            # Retorna uma resposta JSON indicando o erro ocorrido
            return JsonResponse({'status': 'error', 'message': str(e)})

    # Se o método da requisição não for POST, retorne a página normalmente
    return render(request, 'index.html')