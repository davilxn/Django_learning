from django.shortcuts import render, redirect

# Create your views here.
from django.urls import path
from django.http import HttpResponse, Http404
from recipes.models import Category, Recipe
from comments.models import Comments
from comments.forms import CreateComment
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from utils.pagination import make_pagination
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict
from tag.models import Tag
from django.urls import reverse
# OBSERVAÇÃO: Ao utilizar a função Http404, faça 'raise Http404()' e não 'return Http404()' :).

import os
PER_PAGES = os.environ.get('PER_PAGE', 6)

class RecipeListViewBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = 'recipes_list_base'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs) 
        page_obj, pagination_range = make_pagination(self.request, ctx.get('recipes_list_base'), PER_PAGES)
        
        object_cat_title = ctx.get('recipes_list_base').first()
        if object_cat_title is not None:
            title = ctx.get('recipes_list_base').first().category.name
        else:
            title = ''

        ctx.update({
            'recipes': page_obj, 
            'tam': len(ctx.get('recipes_list_base')), 
            'pagination_range': pagination_range, 
            'title': title
            })  
        
        return ctx

class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'   
    

class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'   

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes_list_base']
        recipes_list = recipes.values()
        return JsonResponse(
            list(recipes_list), 
            safe=False
        )

class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/categories.html'
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(category__id=self.kwargs.get('category_id'), is_published=True)
        return qs
    

class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'
    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(Q(
            Q(title__icontains=search_term) | Q(description__icontains=search_term)
            ), is_published=True
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()
        ctx = super().get_context_data(*args, **kwargs) 
        page_obj, pagination_range = make_pagination(self.request, ctx.get('recipes_list_base'), PER_PAGES, 6)
        
        ctx.update({
            'page_title': f'Search for "{search_term}"',
            'search_term': search_term,
            'chave_de_url_adicional': f'&q={search_term}', 
            'searched': page_obj,
            'pagination_range': pagination_range,
            })
        return ctx
    
class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs) 
        page_title = Tag.objects.filter(slug=self.kwargs.get('slug', '')).first()
        
        if not page_title:
            page_title = 'No recipes found'
        
        page_title = f'{page_title} - Tag |'
        ctx.update({
            'page_title': f'"{page_title}"'})
        return ctx

class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe_detail'
    template_name = 'recipes/pages/recipes-view.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        pk = self.kwargs.get('pk')
        this_recipe = Recipe.objects.get(pk=pk, is_published=True)
        form = CreateComment(self.request.POST or None)
        list_comments = Comments.objects.filter(recipe_comment = this_recipe, published_comment=True)
        
        self.context = {
            'form': form,
            'recipe': this_recipe,
            'list_comments': list_comments,
            'comments_count': len(list_comments),
            'is_detail_page': True,
        }

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, context=self.context)
    
    def post(self, *args, **kwargs):
        form = self.context['form']
        
        if form.is_valid:
            comment = form.save(commit=False)

            if self.request.user.is_authenticated:
                comment.user_comment = self.request.user
            else:
                comment.user_comment = 'Annonymous'
            
            comment.recipe_comment = self.context['recipe']
            comment.save()
            messages.success(self.request, 'O comentário foi salvo.')
            return redirect(reverse('recipes-recipe', args=(self.kwargs.get('pk'),)))
        
        return render(self.request, self.template_name, context=self.context)
        
        

        
        

        
            
"""
class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe_detail'
    template_name = 'recipes/pages/recipes-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(pk=self.kwargs.get('pk'), is_published=True)
        return qs
    

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        pk = self.kwargs.get('pk')
        this_recipe = Recipe.objects.get(pk=pk)
        form = CreateComment(self.request.POST or None)
        list_comments = Comments.objects.filter(recipe_comment=ctx.get('recipe_detail')) 
        ctx.update({
            'is_detail_page': True,
            'recipe': ctx.get('recipe_detail'),
            'list_comments': list_comments,
            'form': form
        }) 
        return ctx
"""
class RecipeDetailApi(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe_detail']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = recipe_dict['cover'].url
        else:
            recipe_dict['cover'] = ''


        del recipe_dict['is_published'] 
        del recipe_dict['preparation_steps_is_html']
        return JsonResponse(
            recipe_dict,
            safe=False
        )
    ...

def theory(request, *args, **kwargs):
    recipes = Recipe.objects.values('id', 'title')[:10]
    return render(request, 'recipes/pages/theory.html', context={
        'recipes': recipes
    })

"""
def home(request):
    all_recipes = Recipe.objects.filter(is_published=True).order_by('-id')      # Página principal do site
    page_obj, pagination_range = make_pagination(request, all_recipes, PER_PAGES, 6)

    messages.success(request, 'Parabéns, funcionou!')

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'tam': len(all_recipes),
        'pagination_range': pagination_range,
    })
"""

"""
def category(request, category_id):
    cat = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'))
    page_obj, pagination_range = make_pagination(request, cat, PER_PAGES, 6)
    return render(request, 'recipes/pages/categories.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f"{cat[0].category.name}",
    })
"""

"""
def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    search_recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) | Q(description__icontains=search_term)
        ), is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, search_recipes, PER_PAGES, 6)


    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search for "{search_term}"',
        'search_term': search_term,
        'tam': len(page_obj),
        'searched': page_obj,
        'pagination_range': pagination_range,
        'chave_de_url_adicional': f'&q={search_term}'
    })
"""
"""
def recipes(request, pk):
    rec = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/pages/recipes-view.html ', context={
        'is_detail_page': True,
        'recipe': rec, 
    })
"""

def sobre(request):
    return HttpResponse("Sobre")

def contato(request):
    return HttpResponse("Contato")

