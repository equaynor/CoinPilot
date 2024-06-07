from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    """
    Represents a portfolio owned by a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the portfolio.
        """
        return self.name
