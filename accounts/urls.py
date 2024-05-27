from django.urls import path

from . import initiate_signup_view, login_view, validate_signup_view

urlpatterns = [
    path('signup/initiate', initiate_signup_view.initiate_signup_view,
         name='initiate_signup'),
    path('signup/validate', validate_signup_view.validate_signup_view,
         name='validate_signup'),
    path('login', login_view.login_view, name='login'),
]
