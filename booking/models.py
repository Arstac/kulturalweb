from django.db import models

class Artista(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    contacto = models.EmailField()  # Validación automática de correos electrónicos
    redes_sociales = models.JSONField(default=dict, blank=True)  # Almacena URLs de redes como un diccionario
    imagen = models.ImageField(upload_to='booking/fotos/', null=True, blank=True)
    genero_musical = models.CharField(max_length=100, blank=True, null=True)  # Género musical opcional
    ubicacion = models.CharField(max_length=200, blank=True, null=True)  # Ubicación opcional (ciudad/país)
    sitio_web = models.URLField(blank=True, null=True)  # Página web del artista
    telefono = models.CharField(max_length=15, blank=True, null=True)  # Teléfono opcional
    fecha_inicio = models.DateField(blank=True, null=True)  # Fecha en que comenzó su carrera

    def __str__(self):
        return self.nombre