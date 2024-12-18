from django.db import models
from booking.models import Artista

class CategoriaMusical(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Cancion(models.Model):
    categoria = models.ForeignKey(CategoriaMusical, related_name='canciones', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    url = models.URLField()
    archivo_audio = models.FileField(upload_to='musica/canciones')
    fecha_lanzamiento = models.DateField(null=True, blank=True)  # Campo adicional para la fecha de lanzamiento

    def __str__(self):
        return f"{self.titulo} - {self.artista.nombre}"