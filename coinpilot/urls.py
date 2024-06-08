"""
URL configuration for coinpilot project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('trade/', include('trade.urls')),
]
