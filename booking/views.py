from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Artista
from musica.models import Cancion

def booking(request):
    artistas = Artista.objects.all()
    canciones = Cancion.objects.all()
    contexto = {'mensaje': "Hola, mundo. Este es mi contexto.",
                'artistas': artistas,
                'canciones': canciones}
    return render(request, 'booking/booking.html', contexto)


def artista(request, artista_id):
    artista = get_object_or_404(Artista, pk=artista_id)
    canciones = Cancion.objects.filter(artista=artista)

    eventos_del_artista = artista.eventos.all()

    contexto = {'artista':artista,
                'canciones':canciones,
                'eventos_artista':eventos_del_artista}

    return render(request, 'booking/artista.html', contexto)