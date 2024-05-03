from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Trade
from .forms import TradeForm
from holding.models import Holding

@login_required
def add_trade(request):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            coin = trade.coin

            # Get or create the holding for the selected coin
            holding, created = Holding.objects.get_or_create(portfolio=request.user.portfolio, coin=coin)
            trade.holding = holding

            trade.save()
            return redirect('trade_history')
    else:
        form = TradeForm()
    return render(request, 'trade/add_trade.html', {'form': form})


@login_required
def trade_history(request):
    trades = Trade.objects.filter(holding__portfolio=request.user.portfolio).order_by('-timestamp')
    return render(request, 'trade/trade_history.html', {'trades': trades})