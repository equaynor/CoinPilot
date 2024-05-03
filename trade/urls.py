from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_trade, name='add_trade'),
    # Other URL patterns...
]