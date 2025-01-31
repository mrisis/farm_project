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
    path('my-posts/', views.MyPostListApiView.as_view(), name='my-posts'),

    #post image urls
    path('create-post-image/', views.PostImageCreateApiView.as_view(), name='create-post-image'),
    path('post/<int:post_id>/images/', views.PostImageListApiView.as_view(), name='list-post-images'),
    path('post-images/<int:post_image_id>/update/', views.PostImageUpdateApiView.as_view(), name='post-image-update'),
    path('post-images/<int:post_image_id>/delete/', views.PostImageDeleteApiView.as_view(), name='post-image-delete'),

    #comment urls
    path('create-comment/', views.CommentCreateApiView.as_view(), name='create-comment'),
    path('comment/<int:pk>/detail/', views.CommentDetailApiView.as_view(), name='list-comments'),
    path('comments/<int:post_id>/list/', views.CommentListApiView.as_view(), name='comment-update'),
    path('comment/<int:pk>/update/', views.CommentUpdateApiView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteApiView.as_view(), name='comment-delete'),

    #rating urls
    path('create-rating/', views.RatingCreateApiView.as_view(), name='create-rating'),
    path('rating/<int:pk>/detail/', views.RatingDetailApiView.as_view(), name='rating-detail'),
    path('rating/<int:post_id>/list/', views.RatingListApiView.as_view(), name='rating-update'),
    path('rating/<int:pk>/delete/', views.RatingDeleteApiView.as_view(), name='rating-update'),

    # favourite posts urls
    path('favorite-post/add/', views.FavoritePostAddApiView.as_view(), name='favourite-posts'),
    path('favorite-post/<int:pk>/remove/', views.FavoritePostRemoveApiView.as_view(), name='favourite-posts'),
    path('my-favorite-posts/', views.FavoritePostListApiView.as_view(), name='my-favourite-posts'),


]