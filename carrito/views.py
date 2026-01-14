from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

from tienda.models import Producto, Talla, Modelo
from .models import Carrito, ItemCarrito, Order

@login_required
def carrito(request):
    # Selecciona solo los 2 primeros productos si existen:
    productos = Producto.objects.all()[:2]
    
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        items = carrito.items.all()
        total_articulos = sum(item.cantidad for item in items)
    except Carrito.DoesNotExist:
        carrito = None
        items = []
        total_articulos = 0
    
    return render(request, 'carrito/carrito.html', {
        'carrito': carrito,
        'items': items,
        'productos': productos,
        'total_articulos': total_articulos
    })

@login_required
@login_required
def agregar_producto(request, producto_id):
    if request.method != 'POST':
        return redirect('carrito:carrito')
        
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    
    # Verificar stock si existe
    if hasattr(producto, 'stock') and producto.stock <= 0:
        messages.error(request, f"El producto {producto.nombre} no está disponible.")
        return redirect('tienda:producto', producto_id=producto_id)
    
    # Validación específica para Ropa: Obligar a elegir Talla si existen opciones
    if hasattr(producto, 'ropa'):
        ropa_obj = producto.ropa
        # Si la prenda tiene tallas asociadas y no se ha enviado ninguna
        if ropa_obj.tallas.exists() and not request.POST.get("talla_id"):
            messages.error(request, "Por favor, selecciona una talla.")
            return redirect('tienda:producto', producto_id=producto_id)

    # Validación específica para Ropa: Obligar a elegir Modelo si existen opciones
    if hasattr(producto, 'ropa'):
        ropa_obj = producto.ropa
        if ropa_obj.modelos.exists() and not request.POST.get("modelo_id"):
            messages.error(request, "Por favor, selecciona un modelo.")
            return redirect('tienda:producto', producto_id=producto_id)
    
    talla_id = request.POST.get("talla_id")
    modelo_id = request.POST.get("modelo_id")
    talla = Talla.objects.filter(id=talla_id).first() if talla_id else None
    modelo = Modelo.objects.filter(id=modelo_id).first() if modelo_id else None

    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    item, created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        talla=talla,
        modelo=modelo,
        defaults={'cantidad': 1}
    )

    if not created:
        item.cantidad += 1
        item.save()
        
    return redirect('carrito:carrito')

@login_required
@login_required
def quitar_producto(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()
    return redirect('carrito:carrito')




import stripe
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

# ... existing imports ...

@login_required
def checkout(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        items = carrito.items.all()
        
        if not items.exists():
            messages.warning(request, "Tu carrito está vacío.")
            return redirect('carrito:carrito')
            
        total = carrito.total_carrito()
        
        if total <= 0:
            messages.error(request, "Error en el cálculo del total.")
            return redirect('carrito:carrito')
            
    except Carrito.DoesNotExist:
        messages.warning(request, "No tienes un carrito activo.")
        return redirect('carrito:carrito')
    
    # Crear orden (o recuperar si ya existe pendiente? Por simplicidad creamos una nueva por ahora)
    order = Order.objects.create(
        user=request.user,
        total=total,
        payment_status='Pendiente'
    )
    
    # 1. Configurar PayPal (Legacy)
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": total,
        "item_name": f"Orden #{order.id}",
        "invoice": str(order.id),
        "currency_code": "EUR",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('carrito:payment_success')),
        "cancel_return": request.build_absolute_uri(reverse('carrito:payment_cancel')),
    }
    paypal_form = PayPalPaymentsForm(initial=paypal_dict)
    
    # 2. Contexto para Stripe
    context = {
        'order': order,
        'paypal_form': paypal_form,
        'total': total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY, 
    }
    
    return render(request, 'carrito/checkout.html', context)

@login_required
def update_item_quantity(request, item_id, product_id, quantity):
    item = get_object_or_404(ItemCarrito, id=item_id, producto_id=product_id)
    item.cantidad = int(quantity)
    item.save()

    carrito = item.carrito
    total_carrito = sum(item.subtotal() for item in carrito.items.all())
    total_items = sum(item.cantidad for item in carrito.items.all())  # Total de artículos

    return JsonResponse({
        'subtotal': item.subtotal(),
        'total_carrito': total_carrito,
        'total_items': total_items  # Devuelve el total de artículos en el carrito
    })

@login_required
def create_checkout_session(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        # Actualizar método de pago
        order.payment_method = 'STRIPE'
        order.save()
        
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {
                                'name': f'Orden #{order.id} - LaKultural',
                            },
                            'unit_amount': int(order.total * 100), # En céntimos
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('carrito:payment_success')) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse('carrito:payment_cancel')),
                client_reference_id=str(order.id),
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)


def payment_success(request):
    # Aquí podríamos verificar el session_id con Stripe si queremos feedback inmediato
    # session_id = request.GET.get('session_id')
    return render(request, 'carrito/payment_success.html')

def payment_cancel(request):
    return render(request, 'carrito/payment_cancel.html')