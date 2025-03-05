from django.urls import path

from . import views

urlpatterns = [
    path('access/token/', views.getAccessToken, name='getAccessToken'),
    path('online/lipa/', views.lipa_na_mpesa_online, name='lipaNaMpesaOnline'),

    # register, confirmation, validation and callback URLs
    path('c2b/register/', views.register_urls, name='register_mpesa_validation'),
    path('c2b/confirmation/', views.confirmation, name='confirmation'),
    path('c2b/validation/', views.validation, name='validation'),
    path('c2b/callback/', views.call_back, name='call_back'),
]