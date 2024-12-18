from django.db import models
from usuarios.models import Usuario
from booking.models import Artista

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='eventos/', null=True, blank=True)
    organizador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='eventos_organizados')  # Relación con Usuario
    edad_minima = models.IntegerField(default=18)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    artistas = models.ManyToManyField(Artista, through='ArtistaEvento', related_name='eventos')

    def __str__(self):
        return self.nombre

class ArtistaEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    hora_actuacion = models.TimeField()
    rol = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.artista.nombre} en {self.evento.nombre} a las {self.hora_actuacion}"