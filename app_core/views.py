from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

# Create your views here.

def sendEmail(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        mensagem = request.POST['mensagem']

        # Configuração do e-mail
        remetente = settings.EMAIL_HOST_USER
        destinatario = 'JohnHeroes@outlook.com.br'
        assunto = 'Novo formulário de contato recebido'
        
        # Corpo do e-mail
        texto = f'''
        Nome: {nome}
        E-mail: {email}
        Mensagem: {mensagem}
        '''

        try:
            # Configuração e envio do e-mail
            send_mail(
                subject=assunto,
                message=texto,
                from_email=remetente,
                recipient_list=[destinatario],
                fail_silently=False,
            )

            # Retorna uma resposta JSON indicando sucesso
            return JsonResponse({'status': 'success'})
        except Exception as e:
            # Retorna uma resposta JSON indicando o erro ocorrido
            return JsonResponse({'status': 'error', 'message': str(e)})

    # Se o método da requisição não for POST, retorne a página normalmente
    return render(request, 'index.html')