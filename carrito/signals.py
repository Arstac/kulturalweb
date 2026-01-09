from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings
import logging

from .models import Order, Carrito, OrderItem

logger = logging.getLogger(__name__)

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn_obj = sender
    
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Verificar que el pago sea para nosotros
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            logger.warning(f"IPN recibido con email incorrecto: {ipn_obj.receiver_email}")
            return

        try:
            # El invoice es el ID de la orden
            order_id = int(ipn_obj.invoice)
            order = Order.objects.get(id=order_id)
        except (ValueError, Order.DoesNotExist):
            logger.error(f"IPN recibido para orden inexistente o inválida: {ipn_obj.invoice}")
            return

        # Verificar el monto
        if order.total != ipn_obj.mc_gross:
            logger.error(f"IPN recibido con monto incorrecto. Orden: {order.total}, IPN: {ipn_obj.mc_gross}")
            return

        # Verificar si ya estaba pagada para no procesar doble
        if order.payment_status == 'Completado':
             logger.info(f"Orden #{order.id} ya estaba completada.")
             return

        # Marcar orden como pagada
        order.payment_status = 'Completado'
        order.paypal_transaction_id = ipn_obj.txn_id
        
        # Guardar datos de envío si vienen
        address_parts = [
            ipn_obj.address_name,
            ipn_obj.address_street,
            ipn_obj.address_city,
            ipn_obj.address_state,
            ipn_obj.address_zip,
            ipn_obj.address_country
        ]
        order.shipping_address = ", ".join(filter(None, address_parts))
        order.save()

        # Mover ítems del carrito a la orden y actualizar stock
        try:
            carrito = Carrito.objects.get(usuario=order.user)
            for item in carrito.items.all():
                # Crear OrderItem
                OrderItem.objects.create(
                    order=order,
                    producto=item.producto,
                    nombre_producto=item.producto.nombre,
                    precio=item.producto.precio,
                    cantidad=item.cantidad,
                    talla=item.talla,
                    modelo=item.modelo,
                    nombre_talla=item.talla.nombre if item.talla else None,
                    nombre_modelo=item.modelo.nombre if item.modelo else None
                )
                
                # Actualizar stock
                producto = item.producto
                if producto.stock >= item.cantidad:
                    producto.stock -= item.cantidad
                    producto.save()
                else:
                    logger.warning(f"Stock insuficiente para producto {producto.id} en orden {order.id}")
                    # Aún así procesamos la venta, pero loggeamos el problema.

            # Vaciar carrito
            carrito.items.all().delete()
            logger.info(f"Orden #{order.id} procesada exitosamente.")

        except Carrito.DoesNotExist:
             logger.error(f"No se encontró carrito para el usuario {order.user.username} al procesar orden {order.id}")

    else:
        logger.info(f"IPN recibido con estado no completado: {ipn_obj.payment_status}")
