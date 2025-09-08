
from django.urls import path
from core import views

urlpatterns = [
    path('', views.stockin_list, name='stockin_list'),
    path('create/', views.stockin_create, name='stockin_create'),
]
