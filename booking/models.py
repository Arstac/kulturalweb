from django.db import models

class Artista(models.Model):
    #blank=True permite que el campo sea opcional
    nombre = models.CharField(max_length=100)
    breve_descripcion = models.CharField(max_length=200, blank=True)
    descripcion = models.TextField(blank=True)
    contacto = models.EmailField(blank=True)  # Validación automática de correos electrónicos
    redes_sociales = models.JSONField(default=dict, blank=True)  # Almacena URLs de redes como un diccionario
    imagen = models.ImageField(upload_to='booking/fotos/', null=True, blank=True)
    genero_musical = models.CharField(max_length=100, blank=True, null=True)  # Género musical opcional
    ubicacion = models.CharField(max_length=200, blank=True, null=True)  # Ubicación opcional (ciudad/país)
    sitio_web = models.URLField(blank=True, null=True)  # Página web del artista
    telefono = models.CharField(max_length=15, blank=True, null=True)  # Teléfono opcional
    fecha_inicio = models.DateField(blank=True, null=True)  # Fecha en que comenzó su carrera
    visible = models.BooleanField(default=True)  # Campo nuevo: define si es visible o no
    enlace_soundcloud = models.URLField(blank=True, null=True, help_text="Enlace al perfil o track de SoundCloud del artista")
    enlace_spotify = models.URLField(blank=True, null=True, help_text="Enlace al perfil o track de Spotify del artista")
    enlace_youtube = models.URLField(blank=True, null=True, help_text="Enlace al canal o video de YouTube del artista")
    
    def __str__(self):
        return self.nombre
    