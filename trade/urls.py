from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:portfolio_id>/', views.add_trade, name='add_trade'),
    path('history/<int:portfolio_id>/', views.trade_history, name='trade_history')
]