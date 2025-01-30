from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # auth urls
    path('send-otp/', views.SendOtpApiView.as_view(), name='send_otp'),
    path('verify-otp/', views.VerifyOtpApiView.as_view(), name='verify_otp'),
    path('signup/', views.UserSignupApiView.as_view(), name='signup'),

    # role category url
    path('role-category/create/', views.RoleCategoryCreateApiView.as_view(), name='role_category_create'),
    path('role-category/<int:pk>/detail/', views.RoleCategoryDetailApiView.as_view(), name='role_category_detail'),
    path('role-category/list/', views.RoleCategoryListApiView.as_view(), name='role_category_list'),
    path('role-category/<int:pk>/update/', views.RoleCategoryUpdateApiView.as_view(), name='role_category_update'),
    path('role-category/<int:pk>/delete/', views.RoleCategoryDeleteApiView.as_view(), name='role_category_delete'),


]