from django.db import models

class Artista(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    contacto = models.EmailField()  # Cambiado a EmailField para validar formato de correo
    #redes_sociales = models.JSONField(default=dict)  # Default dict para evitar nulls
    imagen = models.ImageField(upload_to='booking/fotos/', null=True, blank=True)

    def __str__(self):
        return self.nombre