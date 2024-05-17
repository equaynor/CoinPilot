from django.shortcuts import render, redirect, get_object_or_404
from .models import Portfolio
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


def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    user_portfolios = request.user.portfolios.all()

    return render(request, 'portfolio/portfolio.html', {'portfolio': portfolio, 'user_portfolios': user_portfolios})


@login_required
def create_portfolio(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            portfolio = Portfolio.objects.create(user=request.user, name=name)
            messages.success(request, f"Portfolio '{portfolio.name}' created successfully!")
            return JsonResponse({'status': 'success', 'portfolio_id': portfolio.id})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    

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