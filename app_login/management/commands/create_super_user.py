from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Cria um novo superusuário solicitando o email e o nome de usuário.'

    def handle(self, *args, **options):
        email = input('Digite o email do superusuário: ')
        username = input('Digite o nome de usuário do superusuário: ')
        password = input('Digite a senha do superusuário: ')

        try:
            user = User.objects.create_superuser(email=email, username=username, password=password)
            self.stdout.write(self.style.SUCCESS('Superusuário criado com sucesso.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Erro ao criar superusuário: {str(e)}'))
