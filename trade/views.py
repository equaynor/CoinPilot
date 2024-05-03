from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Trade
from .forms import TradeForm

@login_required
def add_trade(request):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.save()
            return redirect('trade_history')
    else:
        form = TradeForm()
    return render(request, 'trade/add_trade.html', {'form': form})