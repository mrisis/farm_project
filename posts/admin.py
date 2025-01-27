from django.contrib import admin
from .models import PostCategory, Post


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'parent']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'slug']
    list_filter = ['parent']


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category']
    search_fields = ['title', 'author', 'category']
    list_filter = ['category', 'author']



admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostAdmin)
