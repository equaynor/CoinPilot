from django.urls import path
from .views import Index
from .views import CustomSignupView


urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
]