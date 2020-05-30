from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('test/', views.api_test, name='api_test'),
    path('input/', views.api_input, name='api_input'),
    path('dict/', views.api_dict, name='api_dict'),
    path('init/', views.api_init, name='api_init'),
    path('resplit/', views.api_resplit, name='api_resplit'),
]