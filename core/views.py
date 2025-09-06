from django.shortcuts import render

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
