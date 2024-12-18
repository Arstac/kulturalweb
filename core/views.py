from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from eventos.models import Evento
from booking.models import Artista
from tienda.models import Producto
from musica.models import Cancion



def artista(request, artista_id):
    artista = get_object_or_404(Artista, pk=artista_id)
    canciones = Cancion.objects.filter(artista=artista)

    eventos_del_artista = artista.eventos.all()

    contexto = {'artista':artista,
                'canciones':canciones,
                'eventos_artista':eventos_del_artista}

    return render(request, 'booking/artista.html', contexto)

    
    
def home(request):
    artistas = Artista.objects.all()
    canciones = Cancion.objects.all()
    eventos = Evento.objects.all()
    
    contexto = {'artistas': artistas, 'canciones': canciones, 'eventos': eventos}
    
    return render(request, 'core/home.html', contexto)



def buscar(request):
    if request.is_ajax():
        query = request.GET.get('term', '')  # 'term' será lo que el usuario está escribiendo
        eventos = Evento.objects.filter(nombre__icontains=query)
        artistas = Artista.objects.filter(nombre__icontains=query)
        productos = Producto.objects.filter(nombre__icontains=query)
        results = []
        for evento in eventos:
            results.append(evento.nombre)
        for artista in artistas:
            results.append(artista.nombre)
        for producto in productos:
            results.append(producto.nombre)
        data = {
            'list': results
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Error: no se realizó una solicitud AJAX"}, status=400)