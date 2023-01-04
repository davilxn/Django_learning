from django.shortcuts import render

# Create your views here.
from django.urls import path
from django.http import HttpResponse

def home(request):        # Página principal do site
    texto = {'nome':'Davizin'}
    return render(request, 'recipes/pages/home.html', context=texto)

def sobre(request):
    return HttpResponse("Sobre")

def contato(request):
    return HttpResponse("Contato")

def recipes(request, id):
    return HttpResponse("Receita de brownie de chocolate:")


