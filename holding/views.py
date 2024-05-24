from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from .models import Holding
from portfolio.models import Portfolio
from trade.models import Trade
from portfolio.views import calculate_profit_loss
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def update_holding(trade):
    print("Entering update_holding function")  # Add this print statement
    
    try:
        holding, created = Holding.objects.get_or_create(portfolio=trade.portfolio, coin=trade.coin, defaults={'quantity': 0})
        
        print(f"Holding: {holding}")  # Add this print statement
        print(f"Created: {created}")  # Add this print statement
        
        if trade.trade_type == 'BUY':
            holding.quantity += trade.quantity
            print(f"Updated holding quantity after buy: {holding.quantity}")  # Add this print statement
        elif trade.trade_type == 'SELL':
            holding.quantity -= trade.quantity
            print(f"Updated holding quantity after sell: {holding.quantity}")  # Add this print statement
        
        holding.save()
        print("Holding saved")  # Add this print statement
    except Exception as e:
        print(f"Error in update_holding function: {str(e)}")  # Add this print statement
    
    print("Exiting update_holding function")  # Add this print statement


@login_required
def holding_detail(request, holding_id):
    # Retrieve the holding and ensure it belongs to the current user
    holding = get_object_or_404(Holding, id=holding_id, portfolio__user=request.user)
    portfolio = holding.portfolio

    # Find the first trade date for this holding's portfolio
    first_trade = Trade.objects.filter(portfolio=holding.portfolio).order_by('date').first()
    first_trade_date = first_trade.date if first_trade else None

    # Calculate holding period in days
    if first_trade_date:
        # Use timezone-aware current time
        now = timezone.now()
        holding_period = (now - first_trade_date).days
    else:
        holding_period = 0

    # Get all trades related to this holding
    trades = Trade.objects.filter(holding=holding).order_by('date')

    context = {
        'holding': holding,
        'holding_period': holding_period,
        'portfolio': portfolio,
        'trades': trades
    }
    return render(request, 'holding/holding_detail.html', context)