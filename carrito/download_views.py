"""
Vistas para descarga segura de productos digitales.
"""
import secrets
from django.http import FileResponse, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import OrderItem


def generate_download_token():
    """Genera un token único para descarga segura."""
    return secrets.token_urlsafe(32)


@login_required
def download_digital_product(request, order_item_id, token):
    """
    Vista para descarga segura de productos digitales.
    
    Verifica:
    - Token válido
    - Pago completado
    - Límite de descargas no alcanzado
    - El usuario es el dueño de la orden
    """
    item = get_object_or_404(
        OrderItem,
        id=order_item_id,
        download_token=token
    )
    
    # Verificar que el usuario es el dueño
    if item.order.user != request.user:
        return HttpResponseForbidden("No tienes permiso para descargar este archivo.")
    
    # Verificar que el pago está completado
    if item.order.payment_status != 'Completado':
        return HttpResponseForbidden("El pago de esta orden no ha sido completado.")
    
    # Verificar límite de descargas
    if item.download_count >= item.max_downloads:
        raise Http404(
            f"Has alcanzado el límite de {item.max_downloads} descargas para este producto. "
            "Contacta con soporte si necesitas ayuda."
        )
    
    # Obtener archivo descargable
    producto = item.producto
    if not producto:
        raise Http404("El producto ya no está disponible.")
    
    archivo = producto.get_archivo_descarga()
    if not archivo:
        raise Http404("Archivo no disponible para descarga.")
    
    # Incrementar contador de descargas
    item.download_count += 1
    item.save(update_fields=['download_count'])
    
    # Determinar nombre de archivo para la descarga
    import os
    filename = os.path.basename(archivo.name)
    
    # Servir archivo
    response = FileResponse(
        archivo.open('rb'),
        as_attachment=True,
        filename=filename
    )
    
    return response


@login_required
def my_downloads(request):
    """
    Vista para que el usuario vea todos sus productos digitales comprados.
    """
    from django.shortcuts import render
    
    # Obtener todos los items digitales de órdenes completadas
    digital_items = OrderItem.objects.filter(
        order__user=request.user,
        order__payment_status='Completado',
        producto__requires_shipping=False,
        download_token__isnull=False
    ).select_related('order', 'producto').order_by('-order__created_at')
    
    return render(request, 'carrito/my_downloads.html', {
        'digital_items': digital_items
    })
