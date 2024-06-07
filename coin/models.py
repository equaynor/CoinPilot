from django.db import models

class Coin(models.Model):
    """
    Model representing a cryptocurrency.
    """
    coin_id = models.CharField(max_length=255, unique=True, default='')
    name = models.CharField(max_length=255, default='')
    symbol = models.CharField(max_length=50, default='')
    current_price = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    image = models.URLField(default='')
    market_cap = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    market_cap_rank = models.IntegerField(default=0)
    price_change_percentage_24h = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ath = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    ath_date = models.DateTimeField(null=True)
    circulating_supply = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    total_supply = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    max_supply = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    categories = models.JSONField(default=list)

    def save(self, *args, **kwargs):
        """
        Saves the Coin instance to the database, converting the symbol to uppercase.
        """
        self.symbol = self.symbol.upper()
        super(Coin, self).save(*args, **kwargs)
        
    def __str__(self):
        """
        Returns a string representation of the Coin instance.
        """
        return self.name
