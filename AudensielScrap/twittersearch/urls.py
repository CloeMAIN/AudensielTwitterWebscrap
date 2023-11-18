# twittersearch/urls.py
from django.urls import path
from . import views

urlpatterns = [
            path('search/<str:mot_cle>/', views.get_tweets, name='search')
        ]
            
