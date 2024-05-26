from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Trade
from holding.models import Holding

@receiver(post_save, sender=Trade)
def update_holding_quantity(sender, instance, **kwargs):
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
    try:
        holding = Holding.objects.get(
            portfolio=instance.portfolio,
            coin=instance.coin
        )
        if instance.trade_type == 'BUY':
            holding.quantity -= instance.quantity
        elif instance.trade_type == 'SELL':
            holding.quantity += instance.quantity

        # Save the updated holding if quantity is not zero. Otherwise, delete it.
        if holding.quantity != 0:
            holding.save()
        else:
            holding.delete()
    except Holding.DoesNotExist:
        pass  # If the holding does not exist, there's nothing to update