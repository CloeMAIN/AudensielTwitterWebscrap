# twittersearch/urls.py
from django.urls import path
from . import views

urlpatterns = [
            path('search/<str:mot_cle>/<str:until_date>/<str:since_date>', views.get_tweets, name='search'),
            path('search_new/<str:req_id>',views.get_dbreq_tweet,name="search_new")
        ]
            
