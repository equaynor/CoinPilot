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


def reverse_holding(temporary_original_trade):
    holding = get_object_or_404(Holding, portfolio=temporary_original_trade.portfolio, coin=temporary_original_trade.coin)
    print(f"Reversing holding for original trade: {temporary_original_trade}")  # Debug print
    print(f"Initial holding quantity: {holding.quantity}")  # Debug print

    if temporary_original_trade.trade_type == 'BUY':
        holding.quantity -= temporary_original_trade.quantity
    elif temporary_original_trade.trade_type == 'SELL':
        holding.quantity += temporary_original_trade.quantity

    print(f"Updated holding quantity after reversal: {holding.quantity}")  # Debug print
    holding.save()


def reinstate_holding(temporary_original_trade):
    holding = get_object_or_404(Holding, portfolio=temporary_original_trade.portfolio, coin=temporary_original_trade.coin)
    print(f"Reinstating holding for original trade: {temporary_original_trade}")  # Debug print
    print(f"Initial holding quantity: {holding.quantity}")  # Debug print

    if temporary_original_trade.trade_type == 'BUY':
        holding.quantity += temporary_original_trade.quantity
    elif temporary_original_trade.trade_type == 'SELL':
        holding.quantity -= temporary_original_trade.quantity

    print(f"Updated holding quantity after reinstation: {holding.quantity}")  # Debug print
    holding.save()


def edit_holding(updated_trade_data):
    portfolio = updated_trade_data['portfolio']
    coin = updated_trade_data['coin']

    try:
        holding = Holding.objects.get(portfolio=portfolio, coin=coin)
        print(f"Found holding: {holding.quantity} {coin} in {portfolio}")

        if updated_trade_data['trade_type'] == 'BUY':
            holding.quantity += Decimal(updated_trade_data['quantity'])
        elif updated_trade_data['trade_type'] == 'SELL':
            print(f"Sell trade: Available quantity: {holding.quantity}, Required quantity: {updated_trade_data['quantity']}")
            if holding.quantity < Decimal(updated_trade_data['quantity']):
                print("Insufficient funds")
                raise ValueError(f"Insufficient funds. Available: {holding.quantity}, Required quantity: {updated_trade_data['quantity']}")

            holding.quantity -= Decimal(updated_trade_data['quantity'])

        holding.save()
        print(f"Saved holding: {holding.quantity} {coin} in {portfolio}")
    except Holding.DoesNotExist:
        raise ValueError("Holding not found")


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

    context = {
        'holding': holding,
        'holding_period': holding_period,
        'portfolio': portfolio
    }
    return render(request, 'holding/holding_detail.html', context)