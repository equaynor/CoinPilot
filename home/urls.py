from django.urls import path
from . import views
from .views import Index, CustomSignupView


urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
]
