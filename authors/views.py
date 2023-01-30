from django.shortcuts import render
from django.http import HttpResponse, Http404
from .forms import RegisterForm

# Create your views here.
def register_view(request):
    form = RegisterForm()
    return render(request, 'authors/pages/register_view.html', context={
        'form': form,
    })

def register_create(request):
    if not request.POST:
        raise Http404()
    form = RegisterForm(request.POST)
    return render(request, 'authors/pages/register_view.html', context={
        'form': form,
    })
