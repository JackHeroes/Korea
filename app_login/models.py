from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Adicione campos personalizados aqui, se necessário.

    # Use o email como campo de autenticação principal
    USERNAME_FIELD = 'email'

    # Certifique-se de que o campo de email seja único
    username = models.CharField(max_length=255, unique=True, default='')
    email = models.EmailField(max_length=255, unique=True, default='')

    # Remova 'email' dos REQUIRED_FIELDS
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
