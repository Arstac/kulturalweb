from django.db import models
from usuarios.models import Usuario
from musica.models import Cancion

class CategoriaArticulo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Modelo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Talla(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    categoria = models.ForeignKey(CategoriaArticulo, related_name='productos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento_activo = models.BooleanField(default=False)
    stock = models.IntegerField(default=0)  # Añadido para control de inventario
    activo = models.BooleanField(default=True)  # Para activar/desactivar productos fácilmente
    modelos = models.ManyToManyField(Modelo, blank=True, related_name='productos')
    tallas = models.ManyToManyField(Talla, blank=True, related_name='productos')
    cancion = models.OneToOneField(Cancion, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes_productos/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"