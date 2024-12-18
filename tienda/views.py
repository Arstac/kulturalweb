from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Producto

def tienda(request):
    productos = Producto.objects.all()
    contexto = {'productos':productos}
    return render(request, 'tienda/tienda.html', contexto)


def producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    #Filtrar productos con la misma CategoriaArticulo
    related_productos = Producto.objects.filter(categoria=producto.categoria).exclude(pk=producto_id)

    contexto = {'producto':producto, 
                'related_productos':related_productos}

    return render(request, 'tienda/producto.html', contexto)