@login_required
def profit_report(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    qs = StockOut.objects.all()
    if start:
        qs = qs.filter(date__gte=start)
    if end:
        qs = qs.filter(date__lte=end)
    from django.db.models import DecimalField
    total_revenue = qs.aggregate(val=Sum(F('unit_price')*F('quantity'), output_field=DecimalField(max_digits=12, decimal_places=2)))['val'] or 0
    total_profit = qs.aggregate(val=Sum((F('unit_price')-F('cost_basis'))*F('quantity'), output_field=DecimalField(max_digits=12, decimal_places=2)))['val'] or 0
    return render(request, 'reports/profit.html', {'items': qs.order_by('-id'), 'total_revenue': total_revenue, 'total_profit': total_profit, 'start': start, 'end': end})
