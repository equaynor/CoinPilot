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
    """
    Add a trade to a portfolio.

    Args:
        request (HttpRequest): The request object.
        portfolio_id (int): The ID of the portfolio.

    Returns:
        HttpResponse: The response object.
    """
    # Print debug message
    print("Entering add_trade view")

    try:
        # Get the portfolio object
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        print(f"Portfolio: {portfolio}")

        if request.method == 'POST':
            # Print debug message
            print("Request method is POST")
            # Create a form instance with the POST data
            form = TradeForm(request.POST)

            if form.is_valid():
                # Print debug message
                print("Form is valid")
                # Save the form data to a trade object
                trade = form.save(commit=False)
                trade.portfolio = portfolio
                # Set the trade date to the current date if not provided
                if not trade.date:
                    trade.date = timezone.now()

                # Temporarily save the trade
                trade.save()
                print(f"Trade saved: {trade}")

                # Calculate the total holdings dynamically
                trades = Trade.objects.filter(
                    portfolio=portfolio, coin=trade.coin)
                total_quantity = sum(
                    t.quantity if t.trade_type == 'BUY'
                    else -t.quantity for t in trades)
                print(f"Calculated total quantity: {total_quantity}")

                if trade.trade_type == 'SELL' and total_quantity < 0:
                    # Print debug message
                    print("Insufficient holdings to perform the sell trade.")
                    # Add an error message to the request
                    messages.error(
                        request,
                        'Insufficient holdings to perform the sell trade.'
                    )
                    # Delete the temporarily saved trade
                    trade.delete()
                else:
                    # Add a success message to the request
                    messages.success(
                        request,
                        f'{trade.trade_type.capitalize()} \
                        trade added successfully.'
                    )
                    # Redirect to the portfolio detail page
                    return redirect(
                        'portfolio_detail',
                        portfolio_id=portfolio_id
                    )
            else:
                # Print debug message
                print("Form is not valid")
                # Print the form errors
                print(f"Form errors: {form.errors}")
        else:
            # Print debug message
            print("Request method is not POST")
            # Create a form instance without data
            form = TradeForm()
    except Exception as e:
        # Print the error message
        print(f"Error in add_trade view: {str(e)}")
        # Get the logger instance
        logger = logging.getLogger(__name__)
        # Log the exception
        logger.exception("An error occurred while adding a trade")
        # Add an error message to the request
        messages.error(
            request,
            'An error occurred while adding the trade. \
            Please check your holdings and try again.')

    # Print debug message
    print("Exiting add_trade view")
    # Render the add trade template with the form and the portfolio object
    return render(
        request,
        'trade/add_trade.html',
        {'form': form, 'portfolio': portfolio}
    )


@login_required
def trade_history(request, portfolio_id):
    """
    Renders the trade history page for a given portfolio.

    Args:
        request (HttpRequest): The HTTP request object.
        portfolio_id (int): The ID of the portfolio.

    Returns:
        HttpResponse: The rendered trade history page.

    Raises:
        Http404: If the portfolio does not exist or the user does not own it.
    """
    try:
        # Get the portfolio object for the given ID
        portfolio = get_object_or_404(
            Portfolio,
            id=portfolio_id,
            user=request.user
        )
        # Get all trades for the portfolio, ordered by date
        trades = Trade.objects.filter(portfolio=portfolio).order_by('-date')

        if request.method == 'POST':
            # Get the filter values from the request
            coin_id = request.POST.get('coin')
            trade_type = request.POST.get('trade_type')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            # Apply the filter values to the trades
            if coin_id:
                trades = trades.filter(coin_id=coin_id)
            if trade_type:
                trades = trades.filter(trade_type=trade_type)
            if start_date:
                trades = trades.filter(timestamp__gte=start_date)
            if end_date:
                trades = trades.filter(timestamp__lte=end_date)

        # Get all coins that have been traded in the portfolio
        coins = Coin.objects.filter(trade__portfolio=portfolio).distinct()

        # Paginate the trades by 10 per page
        paginator = Paginator(trades, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Prepare the context for rendering the template
        context = {
            'portfolio': portfolio,
            'coins': coins,
            'page_obj': page_obj,
        }
        return render(request, 'trade/trade_history.html', context)

    except Exception as e:
        # Log the error and display a message
        messages.error(
            request,
            f"An error occurred while retrieving the trade history: {str(e)}"
        )
        return redirect('portfolio_detail', portfolio_id=portfolio_id)


@login_required
def edit_trade(request, portfolio_id, trade_id):
    """
    Edit a trade in a portfolio.

    Args:
        request (HttpRequest): The HTTP request object.
        portfolio_id (int): The ID of the portfolio.
        trade_id (int): The ID of the trade.

    Returns:
        HttpResponse: The HTTP response object.
    """
    print("Entering edit_trade view")

    try:
        # Get the portfolio and trade objects
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        trade = get_object_or_404(Trade, id=trade_id, portfolio=portfolio)
        print(f"Editing trade: {trade}")

        # Store the original trade quantity in the session
        if 'original_trade_quantity' not in request.session:
            request.session['original_trade_quantity'] = str(trade.quantity)
            request.session['original_trade_type'] = trade.trade_type

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
                trades = Trade.objects.filter(
                    portfolio=portfolio,
                    coin=updated_trade.coin
                )
                total_quantity = sum(
                    t.quantity if t.trade_type == 'BUY'
                    else -t.quantity for t in trades)
                print(f"Calculated total quantity: {total_quantity}")

                if updated_trade.trade_type == 'SELL' and total_quantity < 0:
                    print("Insufficient holdings to perform the sell trade.")
                    messages.error(
                        request,
                        'Insufficient holdings to perform the sell trade.'
                    )

                    # Revert to the original trade quantity
                    updated_trade.quantity = decimal.Decimal(
                        request.session['original_trade_quantity'])
                    updated_trade.trade_type = request.session[
                        'original_trade_type']
                    updated_trade.save()

                    # Clear the session data
                    del request.session['original_trade_quantity']
                    del request.session['original_trade_type']
                else:
                    # Update the holding
                    holding = get_object_or_404(
                        Holding,
                        portfolio=portfolio,
                        coin=updated_trade.coin
                    )
                    holding.quantity = total_quantity
                    holding.save()

                    messages.success(request, f'Trade updated successfully.')

                    # Clear the session data
                    if 'original_trade_quantity' in request.session:
                        del request.session['original_trade_quantity']
                    if 'original_trade_type' in request.session:
                        del request.session['original_trade_type']

                    return redirect(
                        'portfolio_detail',
                        portfolio_id=portfolio_id
                    )
            else:
                print("Form is not valid")
                print(f"Form errors: {form.errors}")
        else:
            # Set the initial value of the coin field to the Coin object
            form = TradeForm(instance=trade, initial={'coin': trade.coin})
    except Exception as e:
        print(f"Error in edit_trade view: {str(e)}")
        logger = logging.getLogger(__name__)
        logger.exception("An error occurred while editing a trade")
        messages.error(
            request,
            'An error occurred while editing the trade. \
            Please check your holdings and try again.'
        )

    print("Exiting edit_trade view")
    return render(
        request,
        'trade/edit_trade.html',
        {'form': form, 'portfolio': portfolio}
    )


@login_required
def delete_trade(request, trade_id):
    """
    Deletes a trade associated with the logged-in user.

    Args:
        request (HttpRequest): The HTTP request object.
        trade_id (int): The ID of the trade to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the portfolio details page
        if the trade is deleted successfully.
        Redirects to the portfolio details page
        with an error message if an error occurs.
    """
    try:
        # Get the trade and ensure it belongs to the logged-in user
        trade = get_object_or_404(Trade, id=trade_id)
        portfolio_id = trade.portfolio.id

        if request.method == 'POST':
            # Delete the trade
            trade.delete()
            messages.success(request, 'Trade deleted successfully.')

            # Determine the redirection target
            next_page = request.GET.get('next', 'portfolio_detail')
            return redirect(next_page, portfolio_id=portfolio_id)

    except Exception as e:
        # Log the error and show a message to the user
        logger = logging.getLogger(__name__)
        logger.exception("An error occurred while deleting a trade")
        messages.error(
            request,
            'An error occurred while deleting the trade. \
            Please try again.'
        )

    # Redirect to the portfolio details page if an error occurs
    return redirect('portfolio_detail', portfolio_id=portfolio_id)
