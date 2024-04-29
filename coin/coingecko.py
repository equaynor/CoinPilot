from django.conf import settings
import requests

class CoinGeckoAPI:
    def __init__(self):
        self.base_url = 'https://api.coingecko.com/api/v3'
        self.api_key = settings.COINGECKO_API

    def get_coins_markets(self):
        url = f"{self.base_url}/coins/markets"
        headers = {
            'Accepts': 'application/json',
            'X-CG-Pro-API-Key': self.api_key
        }
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 250,
            'page': 1,
            'sparkline': False,
            'price_change_percentage': '24h',
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()