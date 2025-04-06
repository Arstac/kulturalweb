from django.urls import path, include
from . import views

app_name = 'carrito' 

urlpatterns = [
    path('', views.carrito, name='carrito'),
    path('agregar/<int:producto_id>/', views.agregar_producto, name='agregar_producto'),
    path('quitar/<int:item_id>/', views.quitar_producto, name='quitar_producto'),     
    path('update/<int:item_id>/<int:product_id>/<int:quantity>/', views.update_item_quantity, name='update_item_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
]