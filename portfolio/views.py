from django.shortcuts import render
from coin.models import Coin

def get_coins():
    coins = Coin.objects.all()
    return coins

def coin_list(request):
    coins = get_coins()  # Fetch the coin data from the database
    context = {
        'coins': coins
    }
    return render(request, 'portfolio/coin_list.html', context)