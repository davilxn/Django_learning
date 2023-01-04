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
    path("Sobre/", views.sobre),
    path("Contato/", views.contato),
    path("", views.home),
    path("recipes/<int:id>", views.recipes)    # Página principal do site
]