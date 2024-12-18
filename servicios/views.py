from django.shortcuts import render

def servicios(request):
    contexto = {'mensaje': "Hola, mundo. Este es mi contexto."}
    return render(request, 'servicios/servicios.html', contexto)