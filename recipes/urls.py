from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from recipes.views import contato, home, sobre

def view_inventada(request):   # Fins didáticos
    return HttpResponse("Essa é uma bela noite para aprender django.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Exemplo/', view_inventada),   # Fins didáticos.
    path("Sobre/", sobre),
    path("Contato/", contato),
    path("Home/", home),
]