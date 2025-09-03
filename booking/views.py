from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import logging
from .forms import ContactoArtistaForm
from .models import Artista, BookingConfig
from musica.models import Cancion

# Configurar logging
logger = logging.getLogger(__name__)

def booking(request):
    artistas = Artista.objects.filter(visible=True)  # Solo artistas visibles
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


@require_POST
def enviar_contacto_artista(request):
    try:
        form = ContactoArtistaForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']

            asunto = f"Nuevo mensaje de {nombre}"
            mensaje_completo = f"Nombre: {nombre}\nEmail: {email}\n\nMensaje:\n{mensaje}"

            config = BookingConfig.objects.first()
            destino = config.email_destino if config else 'contacto@lakultural.eu'

            send_mail(asunto, mensaje_completo, settings.DEFAULT_FROM_EMAIL, [destino])
            return JsonResponse({'ok': True})
        else:
            return JsonResponse({'ok': False, 'errores': form.errors})
    except Exception as e:
        logger.error(f"Error al enviar correo de contacto: {str(e)}", exc_info=True)
        return JsonResponse({'ok': False, 'error': 'Error interno del servidor'})

# def enviar_contacto_artista(request):
#     if request.method == 'POST':
#         form = ContactoArtistaForm(request.POST)
#         if form.is_valid():
#             nombre = form.cleaned_data['nombre']
#             email = form.cleaned_data['email']
#             mensaje = form.cleaned_data['mensaje']

#             asunto = f"Nuevo mensaje de {nombre}"
#             mensaje_completo = f"Nombre: {nombre}\nEmail: {email}\n\nMensaje:\n{mensaje}"
            
#             config = BookingConfig.objects.first()
#             destino = config.email_destino if config else 'kulturalreus@gmail.com'
#             send_mail(asunto, mensaje_completo, settings.DEFAULT_FROM_EMAIL, [destino])

#             return JsonResponse({'ok': True})
#         else:
#             return JsonResponse({'ok': False, 'errores': form.errors})
#     return JsonResponse({'ok': False, 'error': 'Método no permitido'})