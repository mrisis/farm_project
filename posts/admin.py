from django.contrib import admin
from .models import PostCategory, Post, PostImage, Comment, Rating


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
    list_display = ['id','post', 'post_id', 'caption']
    search_fields = ['post', 'caption']
    list_filter = ['post']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','post', 'author', 'parent']
    search_fields = ['post','post_id', 'author', 'author_id']
    list_filter = ['post', 'author']

class RatingAdmin(admin.ModelAdmin):
    list_display = ['id','post','post_id', 'author','author_id', 'score']
    search_fields = ['post','post_id', 'author', 'author_id']
    list_filter = ['post', 'author']

admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Rating, RatingAdmin)
