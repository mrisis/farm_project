from django.urls import path, include
from apps.accounts.views import views_user

app_name = 'accounts'

urlpatterns = [
    # auth urls
    path("api/", include([
        path("v1/accounts/", include([
            path('send-otp/', views_user.SendOtpApiView.as_view(), name='send_otp'),
            path('verify-otp/', views_user.VerifyOtpApiView.as_view(), name='verify_otp'),
            path('signup/', views_user.UserSignupApiView.as_view(), name='signup'),
            path('refresh-token/', views_user.RefreshTokenApiView.as_view(), name='refresh_token'),
            path('profile-info/', views_user.UserProfileInfoApiView.as_view(), name='profile_info'),
            path('profile-update/', views_user.UserProfileUpdateApiView.as_view(), name='profile_update'),

            # role category url

            path('role-category/list/', views_user.RoleCategoryListApiView.as_view(), name='role_category_list'),


            # role urls

            path('role/list/', views_user.RoleListApiView.as_view(), name='role_list'),

            # user address urls

            path('user-address/list/', views_user.UserAddressListApiView.as_view(), name='user_address_list'),
            path('user-address/<int:pk>/detail/', views_user.UserAddressDetailApiView.as_view(), name='user_address_detail'),
            path('user-address/create/', views_user.UserAddressCreateApiview.as_view(), name='user_address_create'),

            # user roles urls

            path('user-roles/list/', views_user.UserRolesListApiView.as_view(), name='user_roles_list'),
            path('user-roles/create/', views_user.UserRoleCreateApiView.as_view(), name='user_roles_create'),
            path('user-roles/<int:pk>/detail/', views_user.UserRoleDetailApiView.as_view(), name='user_roles_detail'),
            path('user-roles/<int:pk>/delete/', views_user.UserRoleDeleteApiView.as_view(), name='user_roles_delete'),
        ]))
    ]))
]