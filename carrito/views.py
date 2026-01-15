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
    """
    Checkout en dos pasos:
    1. Si hay productos físicos, recoger dirección de envío
    2. Mostrar opciones de pago
    """
    try:
        carrito_obj = Carrito.objects.get(usuario=request.user)
        items = carrito_obj.items.select_related('producto').all()
        
        if not items.exists():
            messages.warning(request, "Tu carrito está vacío.")
            return redirect('carrito:carrito')
        
        subtotal = carrito_obj.total_carrito()
        shipping_cost = carrito_obj.shipping_cost()
        total = carrito_obj.total_con_envio()
        
        if subtotal <= 0:
            messages.error(request, "Error en el cálculo del total.")
            return redirect('carrito:carrito')
            
    except Carrito.DoesNotExist:
        messages.warning(request, "No tienes un carrito activo.")
        return redirect('carrito:carrito')
    
    # Determinar si el carrito contiene productos que requieren envío
    requires_shipping = any(item.producto.requires_shipping for item in items)
    
    # Si requiere envío y es POST, procesar formulario de dirección
    from .forms import ShippingAddressForm
    
    if requires_shipping:
        if request.method == 'POST' and 'shipping_submit' in request.POST:
            # Procesar formulario de dirección
            shipping_form = ShippingAddressForm(request.POST)
            if shipping_form.is_valid():
                # Guardar dirección en sesión para usarla al crear la orden
                request.session['shipping_address'] = shipping_form.get_formatted_address()
                request.session['shipping_data'] = shipping_form.cleaned_data
            else:
                # Formulario inválido, mostrar errores
                context = {
                    'shipping_form': shipping_form,
                    'requires_shipping': requires_shipping,
                    'total': total,
                    'items': items,
                    'step': 'shipping',
                }
                return render(request, 'carrito/checkout.html', context)
        
        # Si no hay dirección guardada en sesión, mostrar formulario
        if 'shipping_address' not in request.session:
            shipping_form = ShippingAddressForm()
            context = {
                'shipping_form': shipping_form,
                'requires_shipping': requires_shipping,
                'subtotal': subtotal,
                'shipping_cost': shipping_cost,
                'total': total,
                'items': items,
                'step': 'shipping',
            }
            return render(request, 'carrito/checkout.html', context)
    
    # Paso 2: Crear orden y mostrar opciones de pago
    shipping_address = request.session.pop('shipping_address', None)
    request.session.pop('shipping_data', None)  # Limpiar datos de sesión
    
    order = Order.objects.create(
        user=request.user,
        total=total,
        payment_status='Pendiente',
        requires_shipping=requires_shipping,
        shipping_address=shipping_address or ''
    )
    
    # Configurar PayPal
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
    
    context = {
        'order': order,
        'paypal_form': paypal_form,
        'total': total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'requires_shipping': requires_shipping,
        'shipping_address': shipping_address,
        'step': 'payment',
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
    """
    Página de éxito tras el pago. 
    Para Stripe, verifica la sesión y procesa la orden.
    """
    session_id = request.GET.get('session_id')
    
    if session_id:
        # Pago con Stripe - verificar y procesar
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status == 'paid':
                order_id = int(session.client_reference_id)
                order = Order.objects.get(id=order_id)
                
                # Solo procesar si no está ya completado
                if order.payment_status != 'Completado':
                    order.payment_status = 'Completado'
                    order.stripe_payment_intent = session.payment_intent
                    order.save()
                    
                    # Procesar items del carrito
                    from .signals import process_order_items, send_order_confirmation_email
                    
                    try:
                        carrito = Carrito.objects.get(usuario=order.user)
                        digital_items = process_order_items(order, carrito)
                        carrito.items.all().delete()
                        
                        # Enviar email de confirmación
                        send_order_confirmation_email(order, digital_items)
                        
                    except Carrito.DoesNotExist:
                        pass  # El carrito ya fue procesado
                        
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error procesando pago Stripe: {e}")
    
    return render(request, 'carrito/payment_success.html')


def payment_cancel(request):
    """Página cuando el usuario cancela el pago."""
    return render(request, 'carrito/payment_cancel.html')


@csrf_exempt
def stripe_webhook(request):
    """
    Webhook de Stripe para procesar pagos de forma asíncrona.
    Esto es un backup por si payment_success falla.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)
    
    if not webhook_secret:
        # Sin webhook secret, no podemos verificar la firma
        return HttpResponse(status=400)
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Procesar evento de pago completado
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        if session.get('payment_status') == 'paid':
            try:
                order_id = int(session.get('client_reference_id'))
                order = Order.objects.get(id=order_id)
                
                if order.payment_status != 'Completado':
                    order.payment_status = 'Completado'
                    order.stripe_payment_intent = session.get('payment_intent')
                    order.save()
                    
                    from .signals import process_order_items, send_order_confirmation_email
                    
                    try:
                        carrito = Carrito.objects.get(usuario=order.user)
                        digital_items = process_order_items(order, carrito)
                        carrito.items.all().delete()
                        send_order_confirmation_email(order, digital_items)
                    except Carrito.DoesNotExist:
                        pass
                        
            except (ValueError, Order.DoesNotExist) as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error en webhook Stripe: {e}")
    
    return HttpResponse(status=200)