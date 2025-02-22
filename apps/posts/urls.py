from django.urls import path, include
from apps.posts.views import views_user

app_name = 'posts'

urlpatterns = [
    path("api/", include([
        path("v1/posts/", include([
            # post category urls
            path('list-categories/',views_user.PostCategoryListApiView.as_view(), name='list-categories'),


            #posts urls
            path('create-post/', views_user.PostCreateUserApiView.as_view(), name='create-post'),
            path('list-posts/', views_user.PostListUserApiView.as_view(), name='list-posts'),
            path('post/<int:pk>/detail/', views_user.PostDetailUserApiView.as_view(), name='post-detail'),
            path('post/<int:pk>/update/', views_user.PostUpdateUserApiView.as_view(), name='post-update'),
            path('post/<int:pk>/delete/', views_user.PostDeleteUserApiView.as_view(), name='post-delete'),
            path('my-posts/list/', views_user.MyPostListUserApiView.as_view(), name='my-posts'),
            path('my-posts/<int:pk>/detail/', views_user.MyPostDetailUserApiView.as_view(), name='my-post-detail'),
            path('my-posts/<int:pk>/delete/', views_user.MyPostDeleteApiView.as_view(), name='my-post-delete'),

            #post image urls
            path('create-post-image/', views_user.PostImageCreateUserApiView.as_view(), name='create-post-image'),
            path('post-image/<int:pk>/remove/', views_user.PostImageRemoveApiView.as_view(), name='post-image-remove'),



            path('create-comment-rate/', views_user.PostCommentRateCreateUserApiView.as_view(), name='create-comment'),
            path('comments/rates/<int:post_id>/list/', views_user.PostCommentRateListUserApiView.as_view(), name='comment-update'),
            path('rating-check/', views_user.RatingCheckUserApiView.as_view(), name='rating-check'),

            # favorite post urls
            path('favorite-post/add-or-remove/', views_user.PostAddOrRemoveToFavoriteUserApiView.as_view(), name='add-to-favorite'),
            path('favorite-post/list/', views_user.MyFavoritePostListUserApiView.as_view(), name='favorite-post-list'),
            path('favorite-post/<int:pk>/detail/', views_user.MyFavoritePostDetailUserApiView.as_view(), name='favorite-post-detail'),






        ]))    
    ]))
]