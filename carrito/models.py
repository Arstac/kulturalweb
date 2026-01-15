from django.db import models
from django.conf import settings
from decimal import Decimal
from usuarios.models import Usuario
from tienda.models import Producto, Talla, Modelo


class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="carrito")
    creado_en = models.DateTimeField(auto_now_add=True)

    def total_carrito(self):
        """Subtotal de productos (sin envío)"""
        return sum(item.subtotal() for item in self.items.all())
    
    def has_physical_products(self):
        """Retorna True si hay productos que requieren envío"""
        return any(item.producto.requires_shipping for item in self.items.all())
    
    def shipping_cost(self):
        """Calcula el coste de envío"""
        # Si no hay productos físicos, no hay envío
        if not self.has_physical_products():
            return Decimal('0.00')
        
        subtotal = self.total_carrito()
        threshold = Decimal(str(getattr(settings, 'SHIPPING_FREE_THRESHOLD', 40.00)))
        cost = Decimal(str(getattr(settings, 'SHIPPING_COST', 4.95)))
        
        # Envío gratis si supera el umbral
        if subtotal >= threshold:
            return Decimal('0.00')
        return cost
    
    def total_con_envio(self):
        """Total incluyendo envío"""
        return self.total_carrito() + self.shipping_cost()
    
    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    talla = models.ForeignKey(Talla, null=True, blank=True, on_delete=models.SET_NULL)
    modelo = models.ForeignKey(Modelo, null=True, blank=True, on_delete=models.SET_NULL)

    def subtotal(self):
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre} ({self.talla}, {self.modelo})"

    class Meta:
        unique_together = ['carrito', 'producto', 'talla', 'modelo']
        
class Order(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='Pendiente')
    created_at = models.DateTimeField(auto_now_add=True)
    paypal_transaction_id = models.CharField(max_length=255, blank=True)
    shipping_address = models.TextField(blank=True, null=True, help_text="Dirección de envío")
    
    # Campo para saber si la orden requiere envío físico
    requires_shipping = models.BooleanField(
        default=True,
        verbose_name="Requiere envío",
        help_text="Se calcula automáticamente según los productos del carrito"
    )
    
    PAYMENT_METHOD_CHOICES = [
        ('PAYPAL', 'PayPal'),
        ('STRIPE', 'Stripe'),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='PAYPAL')
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    nombre_producto = models.CharField(max_length=150)  # Guardamos el nombre por si se borra el producto
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)
    
    talla = models.ForeignKey(Talla, null=True, blank=True, on_delete=models.SET_NULL)
    modelo = models.ForeignKey(Modelo, null=True, blank=True, on_delete=models.SET_NULL)
    nombre_talla = models.CharField(max_length=50, blank=True, null=True)
    nombre_modelo = models.CharField(max_length=100, blank=True, null=True)
    
    # Campos para rastrear descargas digitales
    download_token = models.CharField(
        max_length=64, 
        blank=True, 
        null=True,
        verbose_name="Token de descarga",
        help_text="Token único para descarga segura"
    )
    download_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Descargas realizadas"
    )
    max_downloads = models.PositiveIntegerField(
        default=5,
        verbose_name="Máximo de descargas"
    )

    def subtotal(self):
        return self.precio * self.cantidad
    
    def is_digital(self):
        """Retorna True si este item es un producto digital"""
        return self.producto and not self.producto.requires_shipping
    
    def can_download(self):
        """Retorna True si se puede descargar"""
        return (
            self.is_digital() and 
            self.download_token and 
            self.download_count < self.max_downloads and
            self.order.payment_status == 'Completado'
        )

    def __str__(self):
        return f"{self.cantidad} x {self.nombre_producto}"
