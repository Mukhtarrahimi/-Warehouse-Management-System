
from django.urls import path
from core import views

urlpatterns = [
    path('', views.reports_dashboard, name='reports_dashboard'),
    path('profit/', views.profit_report, name='profit_report'),
]
