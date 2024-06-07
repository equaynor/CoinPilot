from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from .models import Holding
from portfolio.models import Portfolio
from trade.models import Trade
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def calculate_profit_loss(holding, trades, current_price):
    """
    Calculate the profit/loss for a holding based on the given trades and current price.

    Args:
        holding (Holding): The holding object.
        trades (QuerySet): The trades related to the holding.
        current_price (float): The current price of the holding's coin.

    Returns:
        dict: A dictionary containing the average purchase price, value, cost, profit/loss,
            and profit/loss percentage.

    Raises:
        ValueError: If the total quantity is zero or negative.
        ZeroDivisionError: If the total quantity is zero.

    """
    try:
        # Calculate the total quantity and total spent
        total_quantity = sum(trade.quantity for trade in trades)
        total_spent = sum(trade.quantity * trade.price for trade in trades)
        
        if total_quantity <= 0:
            raise ValueError("Total quantity is zero or negative, cannot calculate average purchase price.")
        
        # Calculate the average purchase price
        average_purchase_price = total_spent / total_quantity

        # Calculate the value and cost
        value = holding.quantity * current_price
        cost = holding.quantity * average_purchase_price
        
        if cost < 0:
            raise ValueError(f"Unexpected negative cost: {cost}")
        
        # Calculate the profit/loss and profit/loss percentage
        profit_loss = value - cost
        profit_loss_percentage = (profit_loss / cost) * 100 if cost > 0 else 0

        return {
            'average_purchase_price': average_purchase_price,
            'value': value,
            'cost': cost,
            'profit_loss': profit_loss,
            'profit_loss_percentage': profit_loss_percentage
        }
    
    except ZeroDivisionError:
        # Return zero values if the total quantity is zero
        return {
            'average_purchase_price': 0,
            'value': 0,
            'cost': 0,
            'profit_loss': 0,
            'profit_loss_percentage': 0
        }
    except ValueError as e:
        # Optionally log the error or notify through other means
        print(f"Error calculating profit/loss: {e}")
        return {
            'average_purchase_price': 0,
            'value': 0,
            'cost': 0,
            'profit_loss': 0,
            'profit_loss_percentage': 0
        }


@login_required
def holding_detail(request, holding_id):
    """
    Displays detailed information about a specific holding for a user's portfolio,
    including the holding's history of trades, and calculates the profit/loss data.

    Args:
        request (HttpRequest): The HTTP request object.
        holding_id (int): The ID of the holding to display.

    Returns:
        HttpResponse: The rendered holding_detail.html template with the calculated profit/loss data.
    """
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

    # Calculate profit/loss data
    current_price = holding.coin.current_price
    profit_loss_data = calculate_profit_loss(holding, trades, current_price)

    context = {
        'holding': holding,
        'holding_period': holding_period,
        'portfolio': portfolio,
        'trades': trades,
        'profit_loss_data': profit_loss_data
    }
    return render(request, 'holding/holding_detail.html', context)
