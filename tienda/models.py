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
    stock = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    cancion = models.OneToOneField(Cancion, null=True, blank=True, on_delete=models.SET_NULL)
    
    # Campos para diferenciar productos físicos vs digitales
    requires_shipping = models.BooleanField(
        default=True,
        verbose_name="Requiere envío",
        help_text="Desmarcar para productos digitales que no necesitan envío físico"
    )
    archivo_digital = models.FileField(
        upload_to='productos/digitales/',
        blank=True,
        null=True,
        verbose_name="Archivo descargable",
        help_text="Archivo para productos digitales (música, PDF, etc.)"
    )

    def __str__(self):
        return self.nombre
    
    def get_archivo_descarga(self):
        """Retorna el archivo descargable, ya sea archivo_digital o cancion.archivo_audio"""
        if self.archivo_digital:
            return self.archivo_digital
        elif self.cancion and self.cancion.archivo_audio:
            return self.cancion.archivo_audio
        return None

class Ropa(Producto):
    modelos = models.ManyToManyField(Modelo, blank=True, related_name='prenda_ropa')
    tallas = models.ManyToManyField(Talla, blank=True, related_name='prenda_ropa')

    class Meta:
        verbose_name = "Prenda de Ropa"
        verbose_name_plural = "Prendas de Ropa"

class Objeto(Producto):
    class Meta:
        verbose_name = "Objeto / Merch"
        verbose_name_plural = "Objetos / Merch"

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes_productos/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"