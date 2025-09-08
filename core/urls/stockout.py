
from django.urls import path
from core import views

urlpatterns = [
    path('', views.stockout_list, name='stockout_list'),
    path('create/', views.stockout_create, name='stockout_create'),
]
