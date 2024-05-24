from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:holding_id>/', views.holding_detail, name='holding_detail'),
]