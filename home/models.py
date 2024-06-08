from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    UserProfile model associates a User object with a boolean flag
    to indicate whether the user has fetched data from the CoinGecko API.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fetch_coin_data_flag = models.BooleanField(default=False)
