from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404
from authors.forms import RegisterForm, LoginForm, AuthorRecipeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe

# Create your views here.
def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso. Por favor, efetuar login.')
        return redirect('authors-login')

    return render(request, 'authors/pages/register_view.html', context={
        'form': form,
        'form_action': reverse('authors-register')
    })

    ...
"""
def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', context={
        'form': form,
        'form_action': reverse('authors-register-create')
    })

def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Seu usuário foi criado com sucesso. Por favor, efetuar log in.')
        del(request.session['register_form_data'])
        return redirect('authors-login')
    
    return redirect('authors-register')
"""

def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', context={
        'form':form,
        'form_action': reverse('authors-login-create')
    })

def login_create(request):
    if not request.POST:
        raise Http404()
    form = LoginForm(request.POST)
    
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )
        if authenticated_user is not None:
            messages.success(request, 'Login efetuado com sucesso.')
            login(request, authenticated_user)
            
        else:
            messages.error(request, 'Dados incorretos. Por favor, utilize um usuário ou senha válidos.')
    else:
        messages.error(request, 'Erro na validação dos dados.')
    return redirect('authors-dashboard')

@login_required(login_url='authors-login', redirect_field_name='next')
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout efetuado com sucesso.')
    return redirect('authors-login')

@login_required(login_url='authors-login', redirect_field_name='next')
def dashboard(request):
    receitas = Recipe.objects.filter(is_published=False, author=request.user)

    return render(request, 'authors/pages/dashboard.html', context={
        'receitas': receitas,
        'tam': len(receitas),
    })

"""
@login_required(login_url='authors-login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    receita = Recipe.objects.filter(is_published=False, author=request.user, pk=id).first()

    if not receita:
        raise Http404()
    
    form = AuthorRecipeForm(
        data=request.POST or None,  
        files=request.FILES or None,
        instance=receita,
    )

    if form.is_valid():
        receita = form.save(commit=False)     

        receita.author = request.user
        receita.preparation_steps_is_html = False     
        receita.is_published = False

        receita.save()           

        messages.success(request, 'Sua receita foi salva com sucesso')   

        return redirect(reverse('authors-dashboard-recipe-edit', args=(id,)))
    return render(request, 'authors/pages/dashboard_recipe.html', context={
        'form': form,
    })
"""
"""
@login_required(login_url='authors-login', redirect_field_name='next')
def dashboard_recipe_create(request):
    form = AuthorRecipeForm(
        data=request.POST or None,  
        files=request.FILES or None,
    )

    if form.is_valid():
        receita = form.save(commit=False)

        receita.author = request.user
        receita.preparation_steps_is_html = False     
        receita.is_published = False

        receita.save()

        messages.success(request, "A receita foi criada com sucesso.")
        return redirect(reverse('authors-dashboard-recipe-edit', args=(receita.id,)))  
    
    return render(request, 'authors/pages/dashboard_recipe_create.html', context={
        'form': form,
        'form_action': reverse('authors-dashboard-recipe-create')
    })
    """

@login_required(login_url='authors-login', redirect_field_name='next')
def dashboard_recipe_delete(request, id):
    receita = Recipe.objects.filter(is_published=False, author=request.user, pk=id).first()

    if not receita:
        raise Http404()
   
    receita.delete()
    messages.success(request, 'Receita deletada com sucesso.')
    return redirect(reverse('authors-dashboard'))
    