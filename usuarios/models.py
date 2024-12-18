from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Añade campos adicionales personalizados si es necesario
    #foto_perfil = models.ImageField(upload_to='usuarios/fotos/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    #email = models.EmailField(unique = True)
    #fecha_nacimiento = models.DateField(null=True, blank=True)