from django.db import models
from usuarios.models import Usuario
from tienda.models import Producto, Talla, Modelo

class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="carrito")
    creado_en = models.DateTimeField(auto_now_add=True)

    def total_carrito(self):
        return sum(item.subtotal() for item in self.items.all())
    
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
    shipping_address = models.TextField(blank=True, null=True, help_text="Dirección de envío proporcionada por PayPal")

    def __str__(self):
        return f"Orden #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    nombre_producto = models.CharField(max_length=150) # Guardamos el nombre por si se borra el producto
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)
    
    talla = models.ForeignKey(Talla, null=True, blank=True, on_delete=models.SET_NULL)
    modelo = models.ForeignKey(Modelo, null=True, blank=True, on_delete=models.SET_NULL)
    nombre_talla = models.CharField(max_length=50, blank=True, null=True)
    nombre_modelo = models.CharField(max_length=100, blank=True, null=True)

    def subtotal(self):
        return self.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.nombre_producto}"
