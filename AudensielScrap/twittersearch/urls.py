# twittersearch/urls.py
from django.urls import path
from . import views

urlpatterns = [
            #exemple: http://localhost:8000/api/search/taylor/2020-12-02/2018-08-16/20
            path('search/<str:mot_cle>/<str:until_date>/<str:since_date>/<int:nb_tweets>', views.get_tweets, name='search')
        ]
            
