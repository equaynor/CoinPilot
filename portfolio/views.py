from django.shortcuts import render, redirect, get_object_or_404
from .models import Portfolio
from trade.models import Trade
from coin.models import Coin
from holding.views import calculate_profit_loss
from django.db.models import Q
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages


@login_required
def portfolio_redirect(request):
    """
    Redirect the user to the detail page of their first portfolio
    or create a new default portfolio.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the portfolio detail page.
    """
    # Get the user's first portfolio
    portfolio = request.user.portfolios.first()

    # If the user has a portfolio, redirect to its detail page
    if portfolio:
        return redirect('portfolio_detail', portfolio_id=portfolio.id)
    # If the user does not have a portfolio, \
    # create a new default portfolio and redirect to its detail page
    else:
        # Create a new portfolio for the user
        new_portfolio = Portfolio.objects.create(
            user=request.user,
            name='Default Portfolio'
        )
        return redirect('portfolio_detail', portfolio_id=new_portfolio.id)


@login_required
def portfolio_detail(request, portfolio_id):
    """
    Retrieve the portfolio detail page for the given portfolio ID.

    Args:
        request (HttpRequest): The HTTP request object.
        portfolio_id (int): The ID of the portfolio.

    Returns:
        HttpResponse: The rendered portfolio detail page.
    """
    # Retrieve the portfolio object with the given ID \
    # and owned by the current user
    portfolio = get_object_or_404(
        Portfolio, id=portfolio_id, user=request.user)

    # Retrieve all portfolios owned by the current user
    user_portfolios = request.user.portfolios.all()

    # Retrieve all holdings associated with the portfolio \
    # and prefetch the related coin objects
    holdings = portfolio.holdings.all().select_related('coin')

    # Initialize variables to store the total value and cost of the portfolio
    holdings_data = []
    total_value = 0
    total_cost = 0

    # Calculate the profit/loss data for each holding \
    # and store it in the holdings_data list
    for holding in holdings:
        coin = holding.coin
        trades = holding.related_trades.filter(trade_type='BUY')
        current_price = coin.current_price

        profit_loss_data = calculate_profit_loss(
            holding, trades, current_price)

        total_value += profit_loss_data['value']
        total_cost += profit_loss_data['cost']

        holdings_data.append({
            'id': holding.id,
            'coin': coin,
            'quantity': holding.quantity,
            'current_price': current_price,
            'value': profit_loss_data['value'],
            'average_purchase_price': profit_loss_data[
                'average_purchase_price'],
            'profit_loss': profit_loss_data['profit_loss'],
            'profit_loss_percentage': profit_loss_data[
                'profit_loss_percentage']
        })

    # Calculate the overall profit/loss and its percentage
    overall_profit_loss = total_value - total_cost
    overall_profit_loss_percentage = (
        overall_profit_loss / total_cost) * 100 if total_cost > 0 else 0

    # Create a dictionary to store the portfolio summary data
    portfolio_summary = {
        'holdings': holdings_data,
        'total_value': total_value,
        'total_cost': total_cost,
        'overall_profit_loss': overall_profit_loss,
        'overall_profit_loss_percentage': overall_profit_loss_percentage
    }

    # Render the portfolio detail page with the portfolio, \
    # user portfolios, and portfolio summary data
    return render(request, 'portfolio/portfolio.html', {
        'portfolio': portfolio,
        'user_portfolios': user_portfolios,
        'portfolio_summary': portfolio_summary
    })


@login_required
def create_portfolio(request):
    """
    Creates a new portfolio for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the status of the operation
        and the ID of the created portfolio.
    """
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the name of the portfolio from the request data
        name = request.POST.get('name')

        # If a name is provided, \
        # create a new portfolio for the authenticated user
        if name:
            portfolio = Portfolio.objects.create(user=request.user, name=name)

            # Display a success message
            messages.success(
                request, f"Portfolio '{portfolio.name}' created successfully!")

            # Return a JSON response with the status and portfolio ID
            return JsonResponse(
                {'status': 'success', 'portfolio_id': portfolio.id})

    # If the request method is not POST, return an error response
    return JsonResponse(
        {'status': 'error', 'message': 'Invalid request method'})


@login_required
def edit_portfolio(request, portfolio_id):
    """
    Edits an existing portfolio for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.
        portfolio_id (int): The ID of the portfolio to be edited.

    Returns:
        JsonResponse: A JSON response containing the status of the operation
        and the ID of the edited portfolio.
    """
    # Get the portfolio with the specified ID \
    # and owned by the authenticated user
    portfolio = get_object_or_404(
        Portfolio, id=portfolio_id, user=request.user)

    # Check if the request method is POST
    if request.method == 'POST':
        # Get the updated name of the portfolio from the request data
        name = request.POST.get('name')

        # If a name is provided, update the portfolio name and save it
        if name:
            portfolio.name = name
            portfolio.save()

            # Display a success message
            messages.success(
                request, f"Portfolio '{portfolio.name}' updated successfully!")

            # Return a JSON response with the status and portfolio ID
            return JsonResponse(
                {'status': 'success', 'portfolio_id': portfolio.id})

    # If the request method is not POST, return an error response
    return JsonResponse(
        {'status': 'error', 'message': 'Invalid request method'})


@login_required
def delete_portfolio(request, portfolio_id):
    """
    Deletes an existing portfolio for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.
        portfolio_id (int): The ID of the portfolio to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the portfolio redirect page.
    """
    # Get the portfolio with the specified ID \
    # and owned by the authenticated user
    portfolio = get_object_or_404(
        Portfolio, id=portfolio_id, user=request.user)

    # Check if the request method is POST
    if request.method == 'POST':
        # Delete the portfolio
        portfolio.delete()

        # Display a success message
        messages.success(request, "Portfolio deleted successfully.")

        # Redirect to the portfolio redirect page
        return redirect('portfolio_redirect')

    # If the request method is not POST, \
    # display an error message and redirect to the portfolio redirect page
    messages.error(request, "Invalid request method.")
    return redirect('portfolio_redirect')


def coin_list(request):
    """
    Retrieves a list of coins from the cache
    or database based on the query and sort_by parameters
    in the request.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response containing the list of coins.
    """
    # Get the query and sort_by parameters from the request
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by')

    # Generate a cache key based on the query and sort_by parameters
    cache_key = f'coin_list_{query}_{sort_by}'

    # Get the coins from the cache using the cache key
    coins = cache.get(cache_key)

    # If the coins are not found in the cache, retrieve them from the database
    if coins is None:
        coins = Coin.objects.all()

        # Filter the coins based on the query parameter
        if query:
            coins = coins.filter(
                Q(name__icontains=query) | Q(symbol__icontains=query)
            )

        # Sort the coins based on the sort_by parameter
        if sort_by == 'name':
            coins = coins.order_by('name')
        elif sort_by == 'price':
            coins = coins.order_by('-current_price')
        elif sort_by == 'market_cap':
            coins = coins.order_by('-market_cap')
        elif sort_by == 'change_24h':
            coins = coins.order_by('-price_change_percentage_24h')

        # Store the coins in the cache with the cache key for 5 minutes
        cache.set(cache_key, coins, timeout=300)

    # Create the context dictionary containing the coins, \
    # query, and sort_by parameters
    context = {
        'coins': coins,
        'query': query,
        'sort_by': sort_by
    }

    # Render the HTML response using the portfolio/coin_list.html template \
    # and the context dictionary
    return render(request, 'portfolio/coin_list.html', context)
