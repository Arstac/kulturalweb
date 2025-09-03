from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from eventos.models import Evento
from booking.models import Artista
from tienda.models import Producto
from musica.models import Cancion
from django.shortcuts import get_object_or_404



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
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('term', '')
        results = []

        for evento in Evento.objects.filter(nombre__icontains=query)[:5]:
            results.append({'label': evento.nombre, 'url': f"/eventos/{evento.id}", 'type': 'Evento'})

        for artista in Artista.objects.filter(nombre__icontains=query)[:5]:
            results.append({'label': artista.nombre, 'url': f"/booking/artista/{artista.id}", 'type': 'Artista'})

        for producto in Producto.objects.filter(nombre__icontains=query)[:5]:
            results.append({'label': producto.nombre, 'url': f"/tienda/detalle/{producto.id}", 'type': 'Producto'})

        for cancion in Cancion.objects.filter(titulo__icontains=query)[:5]:
            results.append({'label': cancion.titulo, 'url': f"/musica/detalle/{cancion.id}", 'type': 'Canción'})

        return JsonResponse(results, safe=False)
    return JsonResponse({"error": "No es AJAX"}, status=400)
    