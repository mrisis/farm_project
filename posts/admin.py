from django.contrib import admin
from .models import PostCategory, Post, PostImage


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'slug', 'description', 'parent']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'slug']
    list_filter = ['parent']


class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'author', 'category']
    search_fields = ['title', 'author', 'category']
    list_filter = ['category', 'author']


class PostImageAdmin(admin.ModelAdmin):
    list_display = ['id','post', 'post_id', 'image', 'caption']
    search_fields = ['post', 'caption']
    list_filter = ['post']


admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
