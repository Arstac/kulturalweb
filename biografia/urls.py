from django.urls import path
from . import views

app_name = 'biografia' 

urlpatterns = [
    path('', views.biografia, name='biografia'),
]