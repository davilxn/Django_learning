from django.contrib import admin
from .models import Recipe, Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    ...

class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at', 'is_published']
    list_display_links = ['title']
    search_fields = ['id', 'title', 'description', 'preparation_steps']
    list_filter = ['category', 'author', 'is_published', 'preparation_steps_is_html']
    list_per_page = 10
    list_editable = ['is_published']
    ordering = ['-id']
    prepopulated_fields = {
            'slug': ('title',)
          }
    ...

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)