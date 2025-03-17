from django.urls import path, include
from apps.locations.views import views_user
from apps.locations.views import views_admin

app_name = 'locations'

urlpatterns = [
    path("api/", include([
        path("v1/locations/", include([
            # province urls

            path('province/list/', views_user.ProvinceListApiView.as_view(), name='province-list'),


            # city urls

            path('city/list/', views_user.CityListApiView.as_view(), name='city-list'),

            # admin urls
            path("admin/", include([

                # province admin urls
                path('province-list/', views_admin.ProvinceListAdminView.as_view(), name='province-list-admin'),
                path('province-detail/<int:pk>/', views_admin.ProvinceDetailAdminView.as_view(), name='province-detail-admin'),
                path('province-create/', views_admin.ProvinceCreateAdminView.as_view(), name='province-create-admin'),
                path('province-update/<int:pk>/', views_admin.ProvinceUpdateAdminView.as_view(), name='province-update-admin'),
                path('province-delete/<int:pk>/', views_admin.ProvinceDeleteAdminView.as_view(), name='province-delete-admin'),

                # city admin urls
                path('city-list/', views_admin.CityListAdminView.as_view(), name='city-list-admin'),
                path('city-detail/<int:pk>/', views_admin.CityDetailAdminView.as_view(), name='city-detail-admin'),
                path('city-create/', views_admin.CityCreateAdminView.as_view(), name='city-create-admin'),
                path('city-update/<int:pk>/', views_admin.CityUpdateAdminView.as_view(), name='city-update-admin'),
                path('city-delete/<int:pk>/', views_admin.CityDeleteAdminView.as_view(), name='city-delete-admin'),
            ]))
    

        ]))    
    ]))
]