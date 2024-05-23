import threading
from django.core.management.base import BaseCommand
from django.db.models import F
from apscheduler.schedulers.background import BackgroundScheduler
from ...models import Coin
from ...coingecko import CoinGeckoAPI


def fetch_coin_data():
    try:
        api = CoinGeckoAPI()
        coins_data = api.get_coins_markets()

        if coins_data is None:
            print('Failed to fetch coin data from the CoinGecko API')
            return
        else:
            for coin_data in coins_data:
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

    except Exception as e:
        print(f'Error fetching coin data: {e}')
        

class Command(BaseCommand):
    help = 'Fetches and updates coin data from the CoinGecko API'

    def handle(self, *args, **options):
        def run_scheduler():
            scheduler = BackgroundScheduler()
            scheduler.add_job(fetch_coin_data, 'interval', minutes=5)  # Update coin data every 5 minutes
            scheduler.start()
            print('Coin data fetching started.')

        # Start the scheduler in a separate thread
        threading.Thread(target=run_scheduler).start()