from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.booking, name='booking'),
    path('artista/<int:artista_id>/', views.artista, name='artista'),
    path('contacto-artista/', views.enviar_contacto_artista, name='enviar_contacto_artista'),
]