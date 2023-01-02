from django.shortcuts import render

# Create your views here.
from django.urls import path
from django.http import HttpResponse

def sobre(request):
    return HttpResponse("Sobre")

def contato(request):
    return HttpResponse("Contato")

def home(request):
    return HttpResponse("Home")

