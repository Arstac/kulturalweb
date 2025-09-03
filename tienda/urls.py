from django.urls import path
from . import views

app_name = 'tienda' 

urlpatterns = [
    path('', views.tienda, name='tienda'),
    path('<int:producto_id>/', views.producto, name='producto'),
]