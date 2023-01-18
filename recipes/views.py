from django.shortcuts import render

# Create your views here.
from django.urls import path
from django.http import HttpResponse
from recipes.models import Category, Recipe
from django.shortcuts import get_object_or_404

def home(request):
    all_recipes = Recipe.objects.all().order_by('-id')      # Página principal do site
    return render(request, 'recipes/pages/home.html', context={
        'recipes': all_recipes,
    })

def sobre(request):
    return HttpResponse("Sobre")

def contato(request):
    return HttpResponse("Contato")

def recipes(request, id):
    rec = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'recipes/pages/recipes-view.html', context={
        'recipe': rec,
        'is_detail_page': True,
    })


