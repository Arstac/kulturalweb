from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Producto

def tienda(request):
    productos = Producto.objects.filter(activo=True)
    contexto = {'productos': productos}
    return render(request, 'tienda/tienda.html', contexto)


def producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id, activo=True)
    # Filtrar productos con la misma CategoriaArticulo (solo activos)
    related_productos = Producto.objects.filter(
        categoria=producto.categoria, 
        activo=True
    ).exclude(pk=producto_id)[:6]  # Limitamos a 6 relacionados

    contexto = {
        'producto': producto, 
        'related_productos': related_productos
    }

    return render(request, 'tienda/producto.html', contexto)