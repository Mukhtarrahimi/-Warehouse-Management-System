
from django.contrib import admin
from django.urls import path, include
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # login
    path('login/', core_views.login_view, name='login'),
    path('logout/', core_views.logout_view, name='logout'),
    path('', core_views.dashboard, name='dashboard'),
    path('products/', include('core.urls.products')),
    path('suppliers/', include('core.urls.suppliers')),
    path('customers/', include('core.urls.customers')),
    path('stockin/', include('core.urls.stockin')),
    path('stockout/', include('core.urls.stockout')),
    path('reports/', include('core.urls.reports')),
]
