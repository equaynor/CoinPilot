from django.shortcuts import render
from coin.models import Coin
from django.db.models import Q

def coin_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by')
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

    context = {
        'coins': coins,
        'query': query,
        'sort_by': sort_by
    }
    return render(request, 'portfolio/coin_list.html', context)