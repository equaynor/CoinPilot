from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trade
from .forms import TradeForm
from portfolio.models import Portfolio
from holding.models import Holding
from coin.models import Coin
from django.core.exceptions import PermissionDenied

@login_required
def add_trade(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.portfolio = portfolio
            
            coin = trade.coin
            holding, created = Holding.objects.get_or_create(portfolio=portfolio, coin=coin)
            trade.holding = holding
            
            if trade.trade_type == 'buy':
                holding.quantity += trade.quantity
            elif trade.trade_type == 'sell':
                holding.quantity -= trade.quantity
            
            holding.save()
            trade.save()
            
            return redirect('portfolio_detail', portfolio_id=portfolio_id)
    else:
        form = TradeForm()
    return render(request, 'trade/add_trade.html', {'form': form, 'portfolio': portfolio})


@login_required
def trade_history(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    holdings = portfolio.holdings.all()
    trades = Trade.objects.filter(holding__in=holdings).order_by('-timestamp')

    if request.method == 'POST':
        holding_id = request.POST.get('holding')
        if holding_id:
            trades = trades.filter(holding_id=holding_id)

    context = {
        'portfolio': portfolio,
        'holdings': holdings,
        'trades': trades,
    }
    return render(request, 'trade/trade_history.html', context)