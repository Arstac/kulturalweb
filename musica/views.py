from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.templatetags.static import static
from .models import Cancion

def musica(request):
    canciones = Cancion.objects.filter(visible=True)  # Solo artistas visibles
    contexto = {'canciones': canciones}
    return render(request, 'musica/musica.html', contexto)

# def cancion_detalle(request, cancion_id):
#     cancion = get_object_or_404(Cancion, id=cancion_id)
#     data = {
#         'titulo': cancion.titulo,
#         'artista': cancion.artista.nombre,
#         'imagen': request.build_absolute_uri(cancion.album.portada.url) if cancion.album else static('assets/img/default_album.png')
#     }
#     return JsonResponse(data)


def cancion_detalle(request, cancion_id):
    cancion = get_object_or_404(Cancion, id=cancion_id)
    relacionadas = Cancion.objects.filter(artista=cancion.artista, visible=True).exclude(id=cancion.id)[:4]  # Muestra máximo 4
    return render(request, 'musica/cancion_detalle.html', {
        'cancion': cancion,
        'relacionadas': relacionadas,
    })
