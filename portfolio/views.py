from django.shortcuts import render
from coin.models import Coin
from django.db.models import Q
from django.core.cache import cache

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