from django.db import models
from portfolio.models import Portfolio
from holding.models import Holding
from coin.models import Coin
from django.utils import timezone


class Trade(models.Model):
    """
    Represents a single trade done by a user in a portfolio.
    """
    TRADE_TYPE_CHOICES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name='trades', null=True)
    holding = models.ForeignKey(
        Holding,
        on_delete=models.CASCADE,
        related_name='related_trades',
        null=True
    )
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, null=True)
    trade_type = models.CharField(
        max_length=4, choices=TRADE_TYPE_CHOICES, default='BUY')
    quantity = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    price = models.DecimalField(max_digits=18, decimal_places=5, default=0)
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """
        Saves the trade instance, creating a Holding instance if necessary.
        """
        if not self.holding:
            self.holding, created = Holding.objects.get_or_create(
                portfolio=self.portfolio,
                coin=self.coin,
                defaults={'quantity': 0}
            )
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the trade.
        """
        return \
            f"{self.trade_type} {self.quantity} {self.coin.symbol} \
            at {self.price}"
