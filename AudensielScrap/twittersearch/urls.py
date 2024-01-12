# twittersearch/urls.py
from django.urls import path
from . import views

urlpatterns = [
            path('search/<str:mot_cle>/<str:until_date>/<str:since_date>/<int:nb_tweets>', views.get_tweets, name='search')
        ]
            
