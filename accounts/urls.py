from django.urls import path
from . import initiate_signup_view

urlpatterns = [
    path('signup/initiate', initiate_signup_view.initiate_signup,
         name='initiate_signup'),
]
