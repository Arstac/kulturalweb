from django.urls import path, include
from . import views
from . import download_views

app_name = 'carrito' 

urlpatterns = [
    path('', views.carrito, name='carrito'),
    path('agregar/<int:producto_id>/', views.agregar_producto, name='agregar_producto'),
    path('quitar/<int:item_id>/', views.quitar_producto, name='quitar_producto'),     
    path('update/<int:item_id>/<int:product_id>/<int:quantity>/', views.update_item_quantity, name='update_item_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('create-checkout-session/<int:order_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    
    # Descargas digitales
    path('download/<int:order_item_id>/<str:token>/', download_views.download_digital_product, name='download'),
    path('mis-descargas/', download_views.my_downloads, name='my_downloads'),
]