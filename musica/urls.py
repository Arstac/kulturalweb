from django.urls import path
from . import views

app_name = 'musica' 

urlpatterns = [
    path('', views.musica, name='musica'),
    path('musica/cancion_detalle/<int:id>/', views.cancion_detalle, name='cancion_detalle')
]