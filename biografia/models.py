from django.db import models

class Biografia(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    imagenes = models.ImageField(upload_to='biografia/fotos', null=True, blank=True)
    es_visible = models.BooleanField()

    def __str__(self):
        return self.titulo