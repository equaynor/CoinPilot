from django.core.management.base import BaseCommand
from django.db.models import F
from apscheduler.schedulers.background import BackgroundScheduler
from ...models import Coin
from ...coingecko import CoinGeckoAPI

def update_coin_data():
    api = CoinGeckoAPI()
    coins_data = api.get_coins_markets()

    if coins_data is None:
        print('Failed to fetch coin data from the CoinGecko API')
        return
    else:
        print("Type of coins_data:", type(coins_data))
        print("Contents of coins_data:", coins_data)

        for coin_data in coins_data:
            # print("Type of coin_data:", type(coin_data))
            # print("Contents of coin_data:", coin_data)

            coin, created = Coin.objects.update_or_create(
                coin_id=coin_data['id'],
                defaults={
                    'name': coin_data['name'],
                    'symbol': coin_data['symbol'],
                    'current_price': coin_data['current_price'],
                    'image': coin_data['image'],
                    'market_cap': coin_data['market_cap'],
                    'market_cap_rank': coin_data['market_cap_rank'],
                    'price_change_percentage_24h': coin_data.get('price_change_percentage_24h_in_currency'),
                    'ath': coin_data['ath'],
                    'ath_date': coin_data.get('ath_date'),
                    'circulating_supply': coin_data.get('circulating_supply'),
                    'total_supply': coin_data.get('total_supply'),
                    'max_supply': coin_data.get('max_supply'),
                    'categories': coin_data.get('categories', []),
                }
            )

        print('Coin data updated successfully.')

class Command(BaseCommand):
    help = 'Fetches and updates coin data from the CoinGecko API'

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        scheduler.add_job(update_coin_data, 'interval', minutes=5)  # Update coin data every 1 minute
        scheduler.start()

        # Keep the script running indefinitely
        try:
            while True:
                pass
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()