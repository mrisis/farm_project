from django.urls import path
from . import views

app_name = 'locations'
urlpatterns = [
    # province urls
    path('province/create/', views.ProvinceCreateApiView.as_view(), name='province-create'),
    path('province/<int:pk>/detail/', views.ProvinceDetailApiView.as_view(), name='province-detail'),
    path('province/list/', views.ProvinceListApiView.as_view(), name='province-list'),
    path('province/<int:pk>/update/', views.ProvinceUpdateApiView.as_view(), name='province-update'),
    path('province/<int:pk>/delete/', views.ProvinceDeleteApiView.as_view(), name='province-delete'),

]