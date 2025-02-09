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

            # role category url

            path('role-category/list/', views_user.RoleCategoryListApiView.as_view(), name='role_category_list'),


            # role urls

            path('role/list/', views_user.RoleListApiView.as_view(), name='role_list'),
        ]))
    ]))
]