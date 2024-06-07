from django.urls import path
from . import views
from .views import Index, about
from .views import CustomSignupView


urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
]