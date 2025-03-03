from django.urls import path

from . import views

urlpatterns = [
    path('access/token', views.getAccessToken, name='getAccessToken'),
    path('online/lipa', views.lipa_na_mpesa_online, name='lipaNaMpesaOnline'),
]