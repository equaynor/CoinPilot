from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trade
from .forms import TradeForm
from portfolio.models import Portfolio
from holding.models import Holding
from holding.views import update_holding, reverse_holding, edit_holding
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
                if not trade.date:
                    trade.date = timezone.now()
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
def trade_edit(request, trade_id):
    original_trade = get_object_or_404(Trade, id=trade_id)
    form = TradeForm(request.POST or None, instance=original_trade)
    temporary_original_trade = None  # Initialize temporary_original_trade to None

    if request.method == 'GET':
        # Create a temporary trade object with the original trade data
        original_trade_data = {
            'portfolio': original_trade.portfolio.id,
            'coin': original_trade.coin.id,
            'trade_type': original_trade.trade_type,
            'quantity': original_trade.quantity,
            'price': original_trade.price,
            'date': original_trade.date.strftime('%Y-%m-%dT%H:%M:%S')
        }
        
        try:
            temporary_original_trade_id = update_trade(request, original_trade.portfolio.id, original_trade_data)
            print(f"Temporary original trade ID: {temporary_original_trade_id}")  # Debug print
            request.session['temporary_original_trade_id'] = temporary_original_trade_id  # Store the ID in the session
            temporary_original_trade = get_object_or_404(Trade, id=temporary_original_trade_id)
            print(f"Temporary original trade: {temporary_original_trade}")  # Debug print
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('trade_history', portfolio_id=original_trade.portfolio.id)
    
    if request.method == 'POST':
        print(f"Form data: {request.POST}")  # Debug print
        if form.is_valid():
            updated_trade_data = {
                'portfolio': original_trade.portfolio,
                'coin': form.cleaned_data['coin'],
                'trade_type': form.cleaned_data['trade_type'],
                'quantity': form.cleaned_data['quantity'],
                'price': form.cleaned_data['price'],
                'date': form.cleaned_data['date']
            }
            
            temporary_original_trade_id = request.session.get('temporary_original_trade_id')  # Retrieve the ID from the session
            temporary_original_trade = get_object_or_404(Trade, id=temporary_original_trade_id)
            
            print(f"Original trade: {temporary_original_trade}")  # Debug print
            print(f"Updated trade data: {updated_trade_data}")  # Debug print
            
            try:
                # Perform holding updates
                reverse_holding(temporary_original_trade)
                edit_holding(updated_trade_data)
                
                # Update the original trade object with the edited form data
                form = TradeForm(updated_trade_data, instance=original_trade)
                form.save()
                
                # Delete the temporary original trade object
                temporary_original_trade.delete()
                
                print("Trade updated successfully")  # Debug print
                return redirect('trade_history', portfolio_id=original_trade.portfolio.id)
            except ValueError as e:
                # Handle the case when edit_holding raises a ValueError
                messages.error(request, str(e))
                reverse_holding(updated_trade_data)  # Revert the holding quantity back to the original
                temporary_original_trade.delete()  # Delete the temporary original trade object
    
    context = {'form': form, 'trade': original_trade}
    return render(request, 'trade/trade_edit.html', context)


def update_trade(request, portfolio_id, original_trade_data):
    if request.method == 'GET':
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        form = TradeForm(original_trade_data)
        
        if form.is_valid():
            trade = form.save(commit=False)
            trade.portfolio = portfolio
            trade.user = request.user
            trade.save()
            
            print(f"Trade saved: {trade.trade_type} {trade.quantity} {trade.coin.symbol} at {trade.price}")  # Debug print
            
            return trade.id  # Return the trade ID directly
        else:
            raise ValueError(form.errors)  # Raise a ValueError with form errors
    
    raise ValueError('Invalid request method')  # Raise a ValueError for invalid request method