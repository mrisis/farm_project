from django.urls import path, include
from apps.locations.views import views_user

app_name = 'locations'

urlpatterns = [
    path("api/", include([
        path("v1/locations/", include([
            # province urls

            path('province/list/', views_user.ProvinceListApiView.as_view(), name='province-list'),


            # city urls

            path('city/list/', views_user.CityListApiView.as_view(), name='city-list'),


        ]))    
    ]))
]