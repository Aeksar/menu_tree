from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_view, name='main'),
    path('profile/', views.base_view, name='profile'),
    path('about/', views.base_view, name='about'),
    path('settings/', views.base_view, name="pastmain"),
    path('portfolio/', views.base_view, name='portfolio'),
    path('you/', views.base_view, name='you'),
]