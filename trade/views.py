from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trade
from .forms import TradeForm
from portfolio.models import Portfolio
from holding.models import Holding
from coin.models import Coin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
import logging
from django.core.paginator import Paginator


@login_required
def add_trade(request, portfolio_id):
    print("Entering add_trade view")
    
    try:
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        print(f"Portfolio: {portfolio}")
        
        if request.method == 'POST':
            print("Request method is POST")
            form = TradeForm(request.POST)
            
            if form.is_valid():
                print("Form is valid")
                trade = form.save(commit=False)
                trade.portfolio = portfolio
                if not trade.date:
                    trade.date = timezone.now()
                
                # Temporarily save the trade
                trade.save()
                print(f"Trade saved: {trade}")
                
                # Calculate the total holdings dynamically
                trades = Trade.objects.filter(portfolio=portfolio, coin=trade.coin)
                total_quantity = sum(t.quantity if t.trade_type == 'BUY' else -t.quantity for t in trades)
                print(f"Calculated total quantity: {total_quantity}")
                
                if trade.trade_type == 'SELL' and total_quantity < 0:
                    print("Insufficient holdings to perform the sell trade.")
                    messages.error(request, 'Insufficient holdings to perform the sell trade.')
                    trade.delete()  # Delete the temporarily saved trade
                else:
                    messages.success(request, f'{trade.trade_type.capitalize()} trade added successfully.')
                    return redirect('portfolio_detail', portfolio_id=portfolio_id)
            else:
                print("Form is not valid")
                print(f"Form errors: {form.errors}")
        else:
            print("Request method is not POST")
            form = TradeForm()
    except Exception as e:
        print(f"Error in add_trade view: {str(e)}")
        logger = logging.getLogger(__name__)
        logger.exception("An error occurred while adding a trade")
        messages.error(request, 'An error occurred while adding the trade. Please check your holdings and try again.')
    
    print("Exiting add_trade view")
    return render(request, 'trade/add_trade.html', {'form': form, 'portfolio': portfolio})


@login_required
def trade_history(request, portfolio_id):
    try:
        portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
        trades = Trade.objects.filter(portfolio=portfolio).order_by('-date')

        if request.method == 'POST':
            coin_id = request.POST.get('coin')
            trade_type = request.POST.get('trade_type')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            if coin_id:
                trades = trades.filter(coin_id=coin_id)
            if trade_type:
                trades = trades.filter(trade_type=trade_type)
            if start_date:
                trades = trades.filter(timestamp__gte=start_date)
            if end_date:
                trades = trades.filter(timestamp__lte=end_date)

        coins = Coin.objects.filter(trade__portfolio=portfolio).distinct()

        paginator = Paginator(trades, 10)  # Show 10 trades per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'portfolio': portfolio,
            'coins': coins,
            'page_obj': page_obj,
        }
        return render(request, 'trade/trade_history.html', context)

    except Exception as e:
        messages.error(request, f"An error occurred while retrieving the trade history: {str(e)}")
        return redirect('portfolio_detail', portfolio_id=portfolio_id)


@login_required
def edit_trade(request, portfolio_id, trade_id):
    print("Entering edit_trade view")

    try:
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        trade = get_object_or_404(Trade, id=trade_id, portfolio=portfolio)
        print(f"Editing trade: {trade}")

        if request.method == 'POST':
            print("Request method is POST")
            form = TradeForm(request.POST, instance=trade)
            
            if form.is_valid():
                print("Form is valid")
                updated_trade = form.save(commit=False)
                updated_trade.portfolio = portfolio
                
                # Temporarily save the updated trade to check holdings
                updated_trade.save()
                print(f"Updated trade temporarily saved: {updated_trade}")

                # Calculate the total holdings dynamically
                trades = Trade.objects.filter(portfolio=portfolio, coin=updated_trade.coin)
                total_quantity = sum(t.quantity if t.trade_type == 'BUY' else -t.quantity for t in trades)
                print(f"Calculated total quantity: {total_quantity}")

                if updated_trade.trade_type == 'SELL' and total_quantity < 0:
                    print("Insufficient holdings to perform the sell trade.")
                    messages.error(request, 'Insufficient holdings to perform the sell trade.')
                    updated_trade.delete()  # Delete the temporarily saved updated trade
                else:
                    updated_trade.save()
                    messages.success(request, f'Trade updated successfully.')
                    return redirect('portfolio_detail', portfolio_id=portfolio_id)
            else:
                print("Form is not valid")
                print(f"Form errors: {form.errors}")
        else:
            form = TradeForm(instance=trade)
    except Exception as e:
        print(f"Error in edit_trade view: {str(e)}")
        logger = logging.getLogger(__name__)
        logger.exception("An error occurred while editing a trade")
        messages.error(request, 'An error occurred while editing the trade. Please check your holdings and try again.')
    
    print("Exiting edit_trade view")
    return render(request, 'trade/edit_trade.html', {'form': form, 'portfolio': portfolio})


def trade_delete(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id)
    
    if request.method == 'POST':
        try:
            trade.delete()
            messages.success(request, 'Trade deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error deleting trade: {str(e)}')
    else:
        messages.error(request, 'Invalid request method.')
        
    return redirect('trade_history', portfolio_id=trade.portfolio.id)