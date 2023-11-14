# twittersearch/urls.py
from django.urls import path
from .views import get_tweets

urlpatterns = [
    path('tweets/<str:keyword>/', get_tweets, name='get_tweets'),
]
