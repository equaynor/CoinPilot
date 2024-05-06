from django import forms
from .models import Trade
from coin.models import Coin

class TradeForm(forms.ModelForm):
    coin = forms.ModelChoiceField(queryset=Coin.objects.all())

    class Meta:
        model = Trade
        fields = ['coin', 'trade_type', 'quantity', 'price']