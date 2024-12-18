from django.shortcuts import render

def biografia(request):
    contexto = {'mensaje': "Hola, mundo. Este es mi contexto."}
    return render(request, 'biografia/biografia.html', contexto)