from django.contrib import admin
from .models import PostCategory


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'parent']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'slug']
    list_filter = ['parent']


admin.site.register(PostCategory, PostCategoryAdmin)
