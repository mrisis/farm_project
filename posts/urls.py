from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('create-category/', views.PostCategoryCreateApiView.as_view(), name='create-category'),
    path('list-categories/', views.PostCategoryListApiView.as_view(), name='list-categories'),
    path('category/<int:pk>/detail/', views.PostCategoryDetailApiView.as_view(), name='category-detail'),
    path('category/<int:pk>/update/', views.PostCategoryUpdateApiView.as_view(), name='category-update'),
    path('category/<int:pk>/delete/', views.PostCategoryDeleteApiView.as_view(), name='category-delete'),


]