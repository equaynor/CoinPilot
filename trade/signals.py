from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Trade
from holding.models import Holding

@receiver(post_save, sender=Trade)
def update_holding_quantity(sender, instance, **kwargs):
    """
    Updates the quantity of a holding object after a trade is saved.
    If the trade type is 'BUY', the quantity is increased.
    If the trade type is 'SELL', the quantity is decreased.
    """
    holding, created = Holding.objects.get_or_create(
        portfolio=instance.portfolio,
        coin=instance.coin,
        defaults={'quantity': 0}
    )
    if instance.trade_type == 'BUY':
        holding.quantity += instance.quantity
    elif instance.trade_type == 'SELL':
        holding.quantity -= instance.quantity
    
    holding.save()


@receiver(post_delete, sender=Trade)
def handle_trade_deletion(sender, instance, **kwargs):
    """
    Updates the quantity of a holding object after a trade is deleted.
    If the trade type is 'BUY', the quantity is decreased.
    If the trade type is 'SELL', the quantity is increased.
    If the holding does not exist, there's nothing to update.
    """
    try:
        holding = Holding.objects.get(
            portfolio=instance.portfolio,
            coin=instance.coin
        )
        if instance.trade_type == 'BUY':
            holding.quantity -= instance.quantity
        elif instance.trade_type == 'SELL':
            holding.quantity += instance.quantity

        holding.save()

    except Holding.DoesNotExist:
        pass  # If the holding does not exist, there's nothing to update
