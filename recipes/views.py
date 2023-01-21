from django.shortcuts import render

# Create your views here.
from django.urls import path
from django.http import HttpResponse, Http404
from recipes.models import Category, Recipe
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from utils.pagination import make_pagination_range

# OBSERVAÇÃO: Ao utilizar a função Http404, faça 'raise Http404()' e não 'return Http404()' :).

def home(request):
    all_recipes = Recipe.objects.filter(is_published=True).order_by('-id')      # Página principal do site
    #all_recipes = get_list_or_404(Recipe, is_published=True)
    #all_recipes = get_list_or_404(Recipe.objects.filter(is_published=True).order_by('-id'))
    current_page = int(request.GET.get('page', 1))
    paginator = Paginator(all_recipes, 9)
    page_obj = paginator.get_page(current_page)
    pagination_range = make_pagination_range(
        paginator.page_range,
        6, 
        current_page
    )
    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'tam': len(all_recipes),
        'pagination_range': pagination_range,
    })

def recipes(request, id):
    rec = get_object_or_404(Recipe, pk=id)
    return render(request, 'recipes/pages/recipes-view.html ', context={
        'is_detail_page': True,
        'recipe': rec, 
    })

def category(request, category_id):
    #cat = Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id')
    #cat = get_list_or_404(Recipe, category__id=category_id, is_published=True)
    cat = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'))
    return render(request, 'recipes/pages/categories.html', context={
        'recipes': cat,
        'title': f"{cat[0].category.name}"
    })

def search(request):
    search_term = request.GET.get('q').strip()
    search_recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) | Q(description__icontains=search_term)
        ), is_published=True
    ).order_by('-id')

    if not search_term:
        raise Http404()

    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search for "{search_term}"',
        'search_term': search_term,
        'tam': len(search_recipes),
        'searched': search_recipes,
    })

def sobre(request):
    return HttpResponse("Sobre")

def contato(request):
    return HttpResponse("Contato")

