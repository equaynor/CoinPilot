from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trade
from .forms import TradeForm
from portfolio.models import Portfolio
from holding.models import Holding
from holding.views import update_holding
from coin.models import Coin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
import logging
from django.core.paginator import Paginator

@login_required
def add_trade(request, portfolio_id):
    print("Entering add_trade view")  # Add this print statement
    
    try:
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        print(f"Portfolio: {portfolio}")  # Add this print statement
        
        if request.method == 'POST':
            print("Request method is POST")  # Add this print statement
            form = TradeForm(request.POST)
            
            if form.is_valid():
                print("Form is valid")  # Add this print statement
                trade = form.save(commit=False)
                trade.portfolio = portfolio
                trade.save()  # Save the trade first
                print(f"Trade saved: {trade}")  # Add this print statement
                print(f"Trade type: {trade.trade_type}")  
                
                if trade.trade_type == 'BUY':
                    print("Calling update_holding function for buy trade")  # Add this print statement
                    update_holding(trade)
                    print("Returned from update_holding function for buy trade")  # Add this print statement
                    messages.success(request, 'Buy trade added successfully.')
                    return redirect('portfolio_detail', portfolio_id=portfolio_id)
                elif trade.trade_type == 'SELL':
                    holding = get_object_or_404(Holding, portfolio=portfolio, coin=trade.coin)
                    if holding.quantity >= trade.quantity:
                        print("Calling update_holding function for sell trade")  # Add this print statement
                        update_holding(trade)
                        print("Returned from update_holding function for sell trade")  # Add this print statement
                        messages.success(request, 'Sell trade added successfully.')
                        return redirect('portfolio_detail', portfolio_id=portfolio_id)
                    else:
                        messages.error(request, 'Insufficient holdings to perform the sell trade.')
                        trade.delete()  # Delete the trade if insufficient holdings
            else:
                print("Form is not valid")  # Add this print statement
                print(f"Form errors: {form.errors}")  # Add this print statement
        else:
            print("Request method is not POST")  # Add this print statement
            form = TradeForm()
    except Exception as e:
        print(f"Error in add_trade view: {str(e)}")  # Add this print statement
        logger = logging.getLogger(__name__)
        logger.exception("An error occurred while adding a trade")
        messages.error(request, 'An error occurred while adding the trade. Please check your holdings and try again.')
        trade.delete()  # Delete the trade if insufficient holdings
    
    print("Exiting add_trade view")  # Add this print statement
    return render(request, 'trade/add_trade.html', {'form': form, 'portfolio': portfolio})

@login_required
def trade_history(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    trades = Trade.objects.filter(portfolio=portfolio).order_by('-timestamp')

    if request.method == 'POST':
        coin_id = request.POST.get('coin')
        if coin_id:
            trades = trades.filter(coin_id=coin_id)

    coins = Coin.objects.filter(trade__portfolio=portfolio).distinct()

    paginator = Paginator(trades, 10)  # Show 10 trades per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'portfolio': portfolio,
        'coins': coins,
        'page_obj': page_obj,
        'trades': trades,
    }
    return render(request, 'trade/trade_history.html', context)