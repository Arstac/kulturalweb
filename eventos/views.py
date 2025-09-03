from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Evento

def eventos(request):
    # Filtrar solo eventos futuros y ordenarlos por fecha
    eventos = Evento.objects.filter(fecha__gte=timezone.now()).order_by('fecha')
    contexto = {'eventos': eventos}
    return render(request, 'eventos/eventos.html', contexto)


def evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    
    # Obtener eventos relacionados (excluyendo el actual, solo futuros)
    related_eventos = Evento.objects.filter(
        fecha__gte=timezone.now()
    ).exclude(pk=evento_id).order_by('fecha')[:6]

    # Acceder a todos los artistas de este evento (solo visibles)
    artistas_del_evento = evento.artistas.filter(visible=True)

    contexto = {
        'evento': evento, 
        'related_eventos': related_eventos,
        'artistas_del_evento': artistas_del_evento
    }

    return render(request, 'eventos/evento.html', contexto)