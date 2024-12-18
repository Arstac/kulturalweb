from django.shortcuts import render
from django.http import JsonResponse
from .models import Cancion

def musica(request):
    canciones = Cancion.objects.all()
    contexto = {'canciones': canciones}
    return render(request, 'musica/musica.html', contexto)

def cancion_detalle(request, id):
    cancion = Cancion.objects.get(id=id)
    data = {
        'titulo': cancion.titulo,
        'artista': cancion.artista.nombre,  # Asumiendo que artista es un objeto relacionado
        'imagen': cancion.artista.imagen.url  # Asumiendo que tienes un campo de imagen en el modelo
    }
    return JsonResponse(data)