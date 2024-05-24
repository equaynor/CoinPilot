from django.urls import path
from . import views
from .views import trade_delete

urlpatterns = [
    path('add/<int:portfolio_id>/', views.add_trade, name='add_trade'),
    path('history/<int:portfolio_id>/', views.trade_history, name='trade_history'),
    path('trade/<int:trade_id>/edit/', views.edit_trade, name='edit_trade'),
    path('delete/<int:trade_id>/', views.trade_delete, name='trade_delete'),
]