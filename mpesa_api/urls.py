from django.urls import path

from . import views

urlpatterns = [
    path('access/token', views.getAccessToken, name='getAccessToken'),
]