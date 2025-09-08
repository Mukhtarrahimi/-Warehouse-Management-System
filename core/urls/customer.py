@login_required
def profit_report(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    qs = StockOut.objects.all()
    