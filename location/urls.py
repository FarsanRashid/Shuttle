from django.urls import path

from . import recommend_location_view

urlpatterns = [
    path('recommend', recommend_location_view.recommend_location_view,
         name='recommend_location'),]
