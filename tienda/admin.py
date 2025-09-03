from django.contrib import admin
from django.db import models
from .models import Producto, CategoriaArticulo, ImagenProducto,Modelo, Talla

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1  # Número de formas extras mostradas

class ProductoAdmin(admin.ModelAdmin):
    inlines = [
        ImagenProductoInline,
    ]

admin.site.register(Producto, ProductoAdmin)
admin.site.register(CategoriaArticulo)
admin.site.register(Modelo)
admin.site.register(Talla)