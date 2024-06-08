from django.conf import settings
import requests
from requests.exceptions import HTTPError


class CoinGeckoAPI:
    def __init__(self):
        self.base_url = 'https://api.coingecko.com/api/v3'
        self.api_key = settings.COINGECKO_API

    def get_coins_markets(self):
        """
        Retrieves the market data for all coins from the CoinGecko API.

        Returns:
            dict or None: A dictionary containing the market data for all coins
            if the request is successful.
                          Returns None if there is an error fetching the data.

        Raises:
            HTTPError: If there is an error with the HTTP request.

        Notes:
            - The API key for the CoinGecko API is retrieved
            from the Django settings module.
            - The market data is retrieved in USD and sorted
            by market capitalization in descending order.
            - The response is paginated with 250 coins per page
            and only the first page is retrieved.
            - The sparkline data is not included in the response.
            - The price change percentage for the last 24 hours
            is included in the response.
        """
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
            'price_change_percentage': '24h'
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            error_message = \
            f"Error fetching market data from CoinGecko API: {str(e)}"
            print(error_message)
            return None
