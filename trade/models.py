from django.db import models
from holding.models import Holding

class Trade(models.Model):
    holding = models.ForeignKey(Holding, on_delete=models.CASCADE, related_name='trades')
    trade_type = models.CharField(max_length=4, choices=[('BUY', 'Buy'), ('SELL', 'Sell')])
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    price = models.DecimalField(max_digits=18, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trade_type} {self.quantity} {self.holding.coin.symbol} at {self.price}"