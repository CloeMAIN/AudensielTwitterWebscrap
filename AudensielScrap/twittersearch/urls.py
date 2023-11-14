# twittersearch/urls.py
from django.urls import path
from .views import twittersearch

urlpatterns = [
    path('tweets/<str:keyword>/', twittersearch, name='get_tweets'),
]