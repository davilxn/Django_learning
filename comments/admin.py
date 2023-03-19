from django.contrib import admin
from .models import Comments
# Register your models here.
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['title_comment', 'published_comment']
    list_display_links = ['title_comment']
    search_fields = ['title_comment']
    list_filter = ['user_comment']
    list_per_page = 10
    list_editable = ['published_comment']
    ordering = ['-id']

admin.site.register(Comments, CommentsAdmin)