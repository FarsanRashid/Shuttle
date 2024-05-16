from django.urls import path
from . import views

urlpatterns = [
    # Full URL: /api/v1/accounts/signup/
    path('signup', views.signup),
    # Add more endpoints for version 1 here
]
