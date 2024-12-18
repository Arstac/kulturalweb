from django.urls import path
from . import views

app_name = 'usuarios' 

urlpatterns = [
    # path('usuarios/', views.usuarios, name='usuarios'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.ajustes_view, name='ajustes'),
    # Añade más rutas según necesites
]