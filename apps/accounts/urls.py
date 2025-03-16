from django.urls import path, include
from apps.accounts.views import views_user
from apps.accounts.views import views_admin

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
            path('user-address/<int:pk>/update/', views_user.UserAddressUpdateApiView.as_view(), name='user_address_update'),
            path('user-address/<int:pk>/delete/', views_user.UserAddressDeleteApiView.as_view(), name='user_address_delete'),

            # user roles urls

            path('user-roles/list/', views_user.UserRolesListApiView.as_view(), name='user_roles_list'),
            path('user-roles/create/', views_user.UserRoleCreateApiView.as_view(), name='user_roles_create'),
            path('user-roles/<int:pk>/detail/', views_user.UserRoleDetailApiView.as_view(), name='user_roles_detail'),
            path('user-roles/<int:pk>/delete/', views_user.UserRoleDeleteApiView.as_view(), name='user_roles_delete'),

            path('admin/', include([

                # user admin
                path('login/', views_admin.AdminLoginView.as_view(), name='admin_login'),
                path('user-list/', views_admin.UserListAdminView.as_view(), name='user_list'),
                path('user-count/', views_admin.UserCountAdminView.as_view(), name='user_count'),
                path('user-detail/<int:pk>/', views_admin.UserDetailAdminView.as_view(), name='user_detail'),
                path('user-update/<int:pk>/', views_admin.UserUpdateAdminView.as_view(), name='user_update'),
                path('user-create/', views_admin.UserCreateAdminView.as_view(), name='user_create'),
                path('user-delete/<int:pk>/', views_admin.UserDeleteAdminView.as_view(), name='user_delete'),

                # role category admin urls
                path('role-category/list/', views_admin.RoleCategoryListAdminView.as_view(), name='role_category_list'),
                path('role-category/<int:pk>/detail/', views_admin.RoleCategoryDetailAdminView.as_view(), name='role_category_detail'),
                path('role-category/create/', views_admin.RoleCategoryCreateAdminView.as_view(), name='role_category_create'),
                path('role-category/<int:pk>/update/', views_admin.RoleCategoryUpdateAdminView.as_view(), name='role_category_update'),
                path('role-category/<int:pk>/delete/', views_admin.RoleCategoryDeleteAdminView.as_view(), name='role_category_delete'),

                # role admin urls
                path('role-list/', views_admin.RoleListAdminView.as_view(), name='role_list'),
                path('role-detail/<int:pk>/', views_admin.RoleDetailAdminView.as_view(), name='role_detail'),
                path('role-create/', views_admin.RoleCreateAdminView.as_view(), name='role_create'),
                path('role-update/<int:pk>/', views_admin.RoleUpdateAdminView.as_view(), name='role_update'),
                path('role-delete/<int:pk>/', views_admin.RoleDeleteAdminView.as_view(), name='role_delete'),

                # user address admin urls
                path('user-address/list/', views_admin.UserAddressListAdminView.as_view(), name='user_address_list'),
            ]))
        ])),
        

    ]))
]