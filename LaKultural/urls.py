"""LaKultural URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from paypal.standard.ipn import urls as paypal_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path('usuarios/', include ('usuarios.urls')),
    path('tienda/', include ('tienda.urls')),
    path('servicios/', include ('servicios.urls')),
    path('musica/', include ('musica.urls')),
    path('eventos/', include ('eventos.urls')),
    path('booking/', include ('booking.urls')),
    path('biografia/', include ('biografia.urls')),
    path('carrito/', include ('carrito.urls')),
    path('', include ('core.urls')),
    path('paypal/', include(paypal_urls)), 
]
# Sirviendo archivos estáticos y multimedia (en desarrollo, no necesario con Cloudinary)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)