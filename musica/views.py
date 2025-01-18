from django.shortcuts import render
from django.http import JsonResponse
from .models import Cancion

def musica(request):
    canciones = Cancion.objects.filter(visible=True)  # Solo artistas visibles
    contexto = {'canciones': canciones}
    return render(request, 'musica/musica.html', contexto)

def cancion_detalle(request, id):
    # Suponiendo que el objeto existe
    cancion = Cancion.objects.get(id=id)
    data = {
        'titulo': cancion.titulo,
        'artista': cancion.artista.nombre,
        # Para la imagen, primero revisa si el artista tiene la propiedad imagen:
        'imagen': cancion.artista.imagen.url if cancion.artista.imagen else ''
    }
    return JsonResponse(data)