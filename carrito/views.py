from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from tienda.models import Producto
from .models import Carrito, ItemCarrito, Order
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

def carrito(request):
    #selecciona solo los 2 primeros productos si existen:
    productos = Producto.objects.all()
    productos = productos[:2]
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        items = carrito.items.all()
        total_articulos = sum(item.cantidad for item in items)
    except Carrito.DoesNotExist:
        items = []
        total_articulos = 0
    return render(request, 'carrito/carrito.html', {'carrito': carrito,
                                                    'items': items,
                                                    'productos': productos,
                                                    'total_articulos': total_articulos})

def agregar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    item.cantidad += 1
    item.save()
    return redirect('carrito:carrito')

def quitar_producto(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()
    return redirect('carrito:carrito')



def checkout(request):
    carrito = Carrito.objects.get(usuario=request.user)
    items = carrito.items.all()
    total = carrito.total_carrito()
    
    # Crear orden
    order = Order.objects.create(
        user=request.user,
        total=total,
        payment_status='Pendiente'
    )
    
    # Configurar PayPal
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": total,
        "item_name": f"Orden #{order.id}",
        "invoice": str(order.id),
        "currency_code": "EUR",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('payment_success')),
        "cancel_return": request.build_absolute_uri(reverse('payment_cancel')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    
    return render(request, 'carrito/checkout.html', {
        'order': order,
        'form': form,
        'total': total
    })

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
    
def payment_success(request):
    return render(request, 'carrito/payment_success.html')

def payment_cancel(request):
    return render(request, 'carrito/payment_cancel.html')