from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_trade, name='add_trade'),
    path('history/', views.trade_history, name='trade_history'),
]