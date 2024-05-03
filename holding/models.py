from django.db import models
from portfolio.models import Portfolio
from coin.models import Coin

class Holding(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='holdings')
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} {self.coin.symbol} in {self.portfolio.name}"