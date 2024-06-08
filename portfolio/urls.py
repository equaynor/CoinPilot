from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.portfolio_redirect, name='portfolio_redirect'),
    path(
        'details/<int:portfolio_id>/', 
        views.portfolio_detail, 
        name='portfolio_detail'
    ),
    path(
        'create/', 
        views.create_portfolio, 
        name='create_portfolio'
    ),
    path(
        'edit/<int:portfolio_id>/', 
        views.edit_portfolio, 
        name='edit_portfolio'
    ),
    path(
        'delete/<int:portfolio_id>/', 
        views.delete_portfolio, 
        name='delete_portfolio'
    ),
    path(
        'coins/', 
        views.coin_list, 
        name='coin_list'
    ),
    path('holding/', include('holding.urls')),
]