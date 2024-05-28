from django.urls import path
from . import views


urlpatterns = [
    path('add/<int:portfolio_id>/', views.add_trade, name='add_trade'),
    path('history/<int:portfolio_id>/', views.trade_history, name='trade_history'),
    path('<int:portfolio_id>/<int:trade_id>/edit/', views.edit_trade, name='edit_trade'),
    path('delete/<int:trade_id>/', views.delete_trade, name='delete_trade'),
]