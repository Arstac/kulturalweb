"""
Signals para procesar pagos y enviar emails de confirmación.
"""
import secrets
import logging
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from .models import Order, Carrito, OrderItem

logger = logging.getLogger(__name__)


def generate_download_token():
    """Genera un token único para descarga segura."""
    return secrets.token_urlsafe(32)


def process_order_items(order, carrito):
    """
    Mueve los items del carrito a la orden, genera tokens para digitales
    y actualiza el stock.
    
    Returns:
        list: Lista de OrderItems digitales (para incluir en email)
    """
    digital_items = []
    
    for item in carrito.items.select_related('producto').all():
        producto = item.producto
        
        # Determinar si es digital
        is_digital = not producto.requires_shipping
        
        # Crear OrderItem
        order_item = OrderItem.objects.create(
            order=order,
            producto=producto,
            nombre_producto=producto.nombre,
            precio=producto.precio,
            cantidad=item.cantidad,
            talla=item.talla,
            modelo=item.modelo,
            nombre_talla=item.talla.nombre if item.talla else None,
            nombre_modelo=item.modelo.nombre if item.modelo else None,
            # Generar token solo para productos digitales
            download_token=generate_download_token() if is_digital else None,
        )
        
        if is_digital:
            digital_items.append(order_item)
        
        # Actualizar stock
        if producto.stock >= item.cantidad:
            producto.stock -= item.cantidad
            producto.save(update_fields=['stock'])
        else:
            logger.warning(f"Stock insuficiente para producto {producto.id} en orden {order.id}")
    
    return digital_items


def send_order_confirmation_email(order, digital_items=None):
    """
    Envía email de confirmación con resumen de pedido y enlaces de descarga.
    """
    try:
        # Preparar contexto
        base_url = getattr(settings, 'SITE_URL', 'https://lakultural.eu')
        
        context = {
            'order': order,
            'digital_items': digital_items or [],
            'base_url': base_url,
            'current_year': datetime.now().year,
        }
        
        # Renderizar template
        html_message = render_to_string(
            'carrito/emails/order_confirmation.html',
            context
        )
        plain_message = strip_tags(html_message)
        
        # Enviar email
        send_mail(
            subject=f'✅ Confirmación de pedido #{order.id} - LaKultural',
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
        
        logger.info(f"Email de confirmación enviado para orden #{order.id} a {order.user.email}")
        
    except Exception as e:
        logger.error(f"Error enviando email de confirmación para orden #{order.id}: {e}")


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    """Procesa notificaciones IPN de PayPal."""
    ipn_obj = sender
    
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Verificar que el pago sea para nosotros
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            logger.warning(f"IPN recibido con email incorrecto: {ipn_obj.receiver_email}")
            return

        try:
            order_id = int(ipn_obj.invoice)
            order = Order.objects.get(id=order_id)
        except (ValueError, Order.DoesNotExist):
            logger.error(f"IPN recibido para orden inexistente o inválida: {ipn_obj.invoice}")
            return

        # Verificar el monto
        if order.total != ipn_obj.mc_gross:
            logger.error(f"IPN recibido con monto incorrecto. Orden: {order.total}, IPN: {ipn_obj.mc_gross}")
            return

        # Verificar si ya estaba pagada
        if order.payment_status == 'Completado':
            logger.info(f"Orden #{order.id} ya estaba completada.")
            return

        # Marcar orden como pagada
        order.payment_status = 'Completado'
        order.paypal_transaction_id = ipn_obj.txn_id
        
        # Si no hay dirección guardada, usar la de PayPal
        if not order.shipping_address and order.requires_shipping:
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

        # Procesar items del carrito
        try:
            carrito = Carrito.objects.get(usuario=order.user)
            digital_items = process_order_items(order, carrito)
            
            # Vaciar carrito
            carrito.items.all().delete()
            logger.info(f"Orden #{order.id} procesada exitosamente.")
            
            # Enviar email de confirmación
            send_order_confirmation_email(order, digital_items)

        except Carrito.DoesNotExist:
            logger.error(f"No se encontró carrito para el usuario {order.user.username} al procesar orden {order.id}")

    else:
        logger.info(f"IPN recibido con estado no completado: {ipn_obj.payment_status}")
