from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
#from recipes.views import contato, home, sobre
from . import views

def view_inventada(request):   # Fins didáticos
    return HttpResponse("Essa é uma bela noite para aprender django.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Exemplo/', view_inventada),   # Fins didáticos.
    path("Sobre/", views.sobre, name='recipes-sobre'),      # Desnecessário, mas serviu de teste e exemplo
    path("Contato/", views.contato),
    path("", views.RecipeListViewHome.as_view(), name='recipes-home'),
    path("recipes/<int:pk>/", views.RecipeDetail.as_view(), name='recipes-recipe'),   
    path("recipes/category/<int:category_id>/", views.RecipeListViewCategory.as_view(), name='recipes-category'),    
    path("recipes/search/", views.RecipeListViewSearch.as_view(), name='recipes-search'), 
    path("recipes/api/v1", views.RecipeListViewHomeApi.as_view(), name='recipes-home-api-v1'),  
    path("recipes/api/v1/<int:pk>/", views.RecipeDetailApi.as_view(), name='recipes-detail-api-v1'),  
    path('recipes/theory/', views.theory, name='theory')
]