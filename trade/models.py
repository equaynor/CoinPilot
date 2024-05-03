from django.db import models
from holding.models import Holding
from coin.models import Coin

class Trade(models.Model):
    TRADE_TYPE_CHOICES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )

    holding = models.ForeignKey(Holding, on_delete=models.CASCADE, related_name='trades')
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trade_type} {self.quantity} {self.coin.symbol} at {self.price}"