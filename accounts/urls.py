from django.urls import path
from . import views

urlpatterns = [
    path('signup/initiate', views.initiate_signup, name='initiate_signup'),
]
