from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.utils import timezone
from .models import Product, Supplier, Customer, StockIn, StockOut
from .forms import LoginForm, ProductForm, SupplierForm, CustomerForm, StockInForm, StockOutForm
from .permissions import admin_required
# loign
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    total_products = Product.objects.count()
    total_stock = Product.objects.aggregate(s=Sum('stock'))['s'] or 0
    low_stock = Product.objects.filter(stock__lte=F('low_stock_threshold')).count()
    today = timezone.localdate()
    today_sales = StockOut.objects.filter(date=today).aggregate(
        revenue=Sum(ExpressionWrapper(F('unit_price')*F('quantity'), output_field=DecimalField(max_digits=12, decimal_places=2))),
        profit=Sum(ExpressionWrapper((F('unit_price')-F('cost_basis'))*F('quantity'), output_field=DecimalField(max_digits=12, decimal_places=2)))
    )
    context = {
        'total_products': total_products,
        'total_stock': total_stock,
        'low_stock': low_stock,
        'today_revenue': today_sales.get('revenue') or 0,
        'today_profit': today_sales.get('profit') or 0,
    }
    return render(request, 'dashboard.html', context)


# Products
@login_required
def product_list(request):
    q = request.GET.get('q','')
    products = Product.objects.all()
    if q:
        products = products.filter(name__icontains=q) | products.filter(code__icontains=q) | products.filter(category__icontains=q)
    return render(request, 'products/list.html', {'products': products, 'q': q})

@login_required
@admin_required
def product_create(request):
    form = ProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'products/form.html', {'form': form, 'title':'Create Product'})

@login_required
def product_edit(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    if not (request.user.is_superuser or request.user.role == 'ADMIN'):
        # allow staff to only view stock? keep edit for admins
        return redirect('product_list')
    form = ProductForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'products/form.html', {'form': form, 'title':'Edit Product'})

@login_required
@admin_required
def product_delete(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('product_list')
    return render(request, 'confirm_delete.html', {'obj': obj, 'cancel_url':'product_list'})

# Suppliers
@login_required
def supplier_list(request):
    return render(request, 'suppliers/list.html', {'suppliers': Supplier.objects.all()})

@login_required
@admin_required
def supplier_create(request):
    form = SupplierForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(); return redirect('supplier_list')
    return render(request, 'suppliers/form.html', {'form': form, 'title':'Create Supplier'})