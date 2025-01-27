from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    # post category urls
    path('create-category/', views.PostCategoryCreateApiView.as_view(), name='create-category'),
    path('list-categories/', views.PostCategoryListApiView.as_view(), name='list-categories'),
    path('category/<int:pk>/detail/', views.PostCategoryDetailApiView.as_view(), name='category-detail'),
    path('category/<int:pk>/update/', views.PostCategoryUpdateApiView.as_view(), name='category-update'),
    path('category/<int:pk>/delete/', views.PostCategoryDeleteApiView.as_view(), name='category-delete'),

    #posts urls
    path('create-post/', views.PostCreateApiView.as_view(), name='create-post'),
    path('list-posts/', views.PostListApiView.as_view(), name='list-posts'),
    path('post/<int:pk>/detail/', views.PostDetailApiView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateApiView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteApiView.as_view(), name='post-delete'),

    #post image urls
    path('create-post-image/', views.PostImageCreateApiView.as_view(), name='create-post-image'),
    path('post/<int:post_id>/images/', views.PostImageListApiView.as_view(), name='list-post-images'),
    path('post-images/<int:post_image_id>/update/', views.PostImageUpdateApiView.as_view(), name='post-image-update'),
    path('post-images/<int:post_image_id>/delete/', views.PostImageDeleteApiView.as_view(), name='post-image-delete'),


]