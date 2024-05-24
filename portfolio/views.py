from django.shortcuts import render, redirect, get_object_or_404
from .models import Portfolio
from trade.models import Trade
from coin.models import Coin
from django.db.models import Q
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages


@login_required
def portfolio_redirect(request):
    portfolio = request.user.portfolios.first()
    if portfolio:
        return redirect('portfolio_detail', portfolio_id=portfolio.id)
    else:
        # Create a new portfolio for the user
        new_portfolio = Portfolio.objects.create(user=request.user, name='My Portfolio')
        return redirect('portfolio_detail', portfolio_id=new_portfolio.id)


@login_required
def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    user_portfolios = request.user.portfolios.all()

    holdings = portfolio.holdings.all().select_related('coin')
    holdings_data = []
    total_value = 0
    total_cost = 0

    for holding in holdings:
        coin = holding.coin
        trades = Trade.objects.filter(portfolio=portfolio, coin=coin, trade_type='BUY')
        current_price = coin.current_price

        profit_loss_data = calculate_profit_loss(holding, trades, current_price)

        total_value += profit_loss_data['value']
        total_cost += profit_loss_data['cost']

        holdings_data.append({
            'id': holding.id,
            'coin': coin,
            'quantity': holding.quantity,
            'current_price': current_price,
            'value': profit_loss_data['value'],
            'average_purchase_price': profit_loss_data['average_purchase_price'],
            'profit_loss': profit_loss_data['profit_loss'],
            'profit_loss_percentage': profit_loss_data['profit_loss_percentage']
        })

    overall_profit_loss = total_value - total_cost
    overall_profit_loss_percentage = (overall_profit_loss / total_cost) * 100 if total_cost > 0 else 0

    portfolio_summary = {
        'holdings': holdings_data,
        'total_value': total_value,
        'total_cost': total_cost,
        'overall_profit_loss': overall_profit_loss,
        'overall_profit_loss_percentage': overall_profit_loss_percentage
    }

    return render(request, 'portfolio/portfolio.html', {
        'portfolio': portfolio,
        'user_portfolios': user_portfolios,
        'portfolio_summary': portfolio_summary
    })


def calculate_profit_loss(holding, trades, current_price):
    try:
        total_quantity = sum(trade.quantity for trade in trades)
        total_spent = sum(trade.quantity * trade.price for trade in trades)
        
        if total_quantity <= 0:
            raise ValueError("Total quantity is zero or negative, cannot calculate average purchase price.")
        
        average_purchase_price = total_spent / total_quantity

        value = holding.quantity * current_price
        cost = holding.quantity * average_purchase_price
        
        if cost < 0:
            raise ValueError(f"Unexpected negative cost: {cost}")
        
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
def create_portfolio(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            portfolio = Portfolio.objects.create(user=request.user, name=name)
            messages.success(request, f"Portfolio '{portfolio.name}' created successfully!")
            return JsonResponse({'status': 'success', 'portfolio_id': portfolio.id})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def delete_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    if request.method == 'POST':
        portfolio.delete()
        messages.success(request, "Portfolio deleted successfully.")
        return redirect('portfolio_redirect')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('portfolio_redirect')


def coin_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by')
    cache_key = f'coin_list_{query}_{sort_by}'
    coins = cache.get(cache_key)

    if coins is None:
        coins = Coin.objects.all()

        if query:
            coins = coins.filter(
                Q(name__icontains=query) | Q(symbol__icontains=query)
            )

        if sort_by == 'name':
            coins = coins.order_by('name')
        elif sort_by == 'price':
            coins = coins.order_by('-current_price')
        elif sort_by == 'market_cap':
            coins = coins.order_by('-market_cap')
        elif sort_by == 'change_24h':
            coins = coins.order_by('-price_change_percentage_24h')

        cache.set(cache_key, coins, timeout=300)  # Cache for 5 minutes

    context = {
        'coins': coins,
        'query': query,
        'sort_by': sort_by
    }
    return render(request, 'portfolio/coin_list.html', context)