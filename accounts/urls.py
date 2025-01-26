from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('send-otp/', views.SendOtpApiView.as_view(), name='send_otp'),
    path('verify-otp/', views.VerifyOtpApiView.as_view(), name='verify_otp'),
    path('signup/', views.UserSignupApiView.as_view(), name='signup'),

]