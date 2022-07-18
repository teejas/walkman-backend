from django.urls import path

from . import views

urlpatterns = [
    path('get_token/', views.get_token, name='get_token'),
    path('connect_device/', views.connect_device, name='connect_device'),
    path('get_recommendations/', views.get_recommendations, name='get_recommendations'),
]