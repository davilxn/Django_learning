from django.views import View
from recipes.models import Recipe
from django.http.response import Http404
from authors.forms import AuthorRecipeForm
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required(login_url='authors-login', redirect_field_name='next'), name='dispatch')
class DashboardRecipeView(View):
    def get_recipe(self, id=None):
        receita = None

        if id is not None:
            receita = Recipe.objects.filter(is_published=False, author=self.request.user, pk=id).first()

            if not receita:
                raise Http404()
        
        return receita
    

    def render_recipe(self, form):
        return render(self.request, 'authors/pages/dashboard_recipe.html', context={
            'form': form,
        })

    
    def get(self, request, id=None):
        receita = self.get_recipe(id)
        form = AuthorRecipeForm(instance=receita)
        return self.render_recipe(form)

    def post(self, request, id=None):
        receita = self.get_recipe(id)
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

            return redirect(reverse('authors-dashboard-recipe-edit', args=(receita.id,)))
        return self.render_recipe(form)

        ...
@method_decorator(login_required(login_url='authors-login', redirect_field_name='next'), name='dispatch')
class DashboardRecipeDelete(DashboardRecipeView):
    def post(self, request, id=None):
        receita = self.get_recipe(id)
        receita.delete()
        messages.success(self.request, 'Receita deletada com sucesso.')
        return redirect(reverse('authors-dashboard'))