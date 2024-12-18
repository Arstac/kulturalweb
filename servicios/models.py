from django.db import models

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # Opcional, en caso de tener servicios con precio fijo
    disponible = models.BooleanField(default=True)  # Para controlar la disponibilidad del servicio

    def __str__(self):
        return self.nombre