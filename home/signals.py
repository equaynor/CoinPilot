from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.management import call_command

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(user_logged_in)
def set_fetch_coin_data_flag(sender, request, user, **kwargs):
    user.userprofile.fetch_coin_data_flag = True
    user.userprofile.save()
    call_command('fetch_coin_data')

@receiver(user_logged_out)
def unset_fetch_coin_data_flag(sender, request, user, **kwargs):
    user.userprofile.fetch_coin_data_flag = False
    user.userprofile.save()