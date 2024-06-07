from django import forms
from .models import Trade
from coin.models import Coin
from django.utils import timezone

class TradeForm(forms.ModelForm):
    """
    Form for creating and updating Trades.
    """
    coin = forms.ModelChoiceField(queryset=Coin.objects.all())
    quantity = forms.DecimalField(max_digits=18, decimal_places=8)
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now,
        required=False
    )

    class Meta:
        model = Trade
        fields = ['coin', 'trade_type', 'quantity', 'price', 'date']
