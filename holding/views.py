from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Holding
from trade.models import Trade

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