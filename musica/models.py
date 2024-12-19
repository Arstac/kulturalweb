from django.db import models
from booking.models import Artista

class CategoriaMusical(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Album(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)  # Opcional
    artistas = models.ManyToManyField(Artista, related_name='albumes_colaborativos', blank=True)  # Colaboradores opcionales
    fecha_lanzamiento = models.DateField()
    portada = models.ImageField(upload_to='musica/portadas', blank=True, null=True)  # Imagen de portada
    categoria = models.ForeignKey(CategoriaMusical, on_delete=models.SET_NULL, null=True, blank=True)  # Categoría del álbum

    def __str__(self):
        return self.titulo

class Cancion(models.Model):
    titulo = models.CharField(max_length=100)
    categoria = models.ForeignKey(CategoriaMusical, related_name='canciones', on_delete=models.CASCADE)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name='canciones', on_delete=models.SET_NULL, null=True, blank=True)  # Opcional
    url = models.URLField(blank=True, null=True)  # URL opcional
    archivo_audio = models.FileField(upload_to='musica/canciones')
    fecha_lanzamiento = models.DateField(null=True, blank=True)
    visible = models.BooleanField(default=True)  # Campo nuevo: define si es visible o no


    def __str__(self):
        album_info = f" ({self.album.titulo})" if self.album else ""
        return f"{self.titulo} - {self.artista.nombre}{album_info}"