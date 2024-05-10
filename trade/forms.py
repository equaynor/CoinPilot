from django import forms
from .models import Trade
from coin.models import Coin
from django.utils import timezone

class TradeForm(forms.ModelForm):
    coin = forms.ModelChoiceField(queryset=Coin.objects.all())
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now,
        required=False
    )

    class Meta:
        model = Trade
        fields = ['coin', 'trade_type', 'quantity', 'price', 'date']