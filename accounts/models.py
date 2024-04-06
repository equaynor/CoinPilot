from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)

    # Customize the `username` field to allow null values
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)

    # Set the `email` field as the `USERNAME_FIELD`
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email