from django.conf import settings
import requests
from requests.exceptions import HTTPError

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
            'sparkline': 'false',
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            error_message = f"Error fetching market data from CoinGecko API: {str(e)}"
            print(error_message)
            return None